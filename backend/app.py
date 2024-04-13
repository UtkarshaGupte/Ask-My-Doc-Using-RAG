from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from operator import itemgetter

from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter


import time
import asyncio
import os


class MyApp(FastAPI):

    def __init__(self):
        super().__init__()
        self.global_retriever = None
        self.setup()

    def setup(self):

        origins = [
            "http://localhost",
            "http://localhost:8501",  # Update with your frontend URL
        ]

        self.add_middleware(
            CORSMiddleware,
            allow_origins= origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.MODEL = "llama2"
        self.model = Ollama(model=self.MODEL)
        self.embeddings = OllamaEmbeddings(model=self.MODEL)

        self.parser = StrOutputParser()


        # Define the prompt template
        self.template = """
        Answer the question based on the context below. If you can't 
        answer the question, reply "I don't know".

        Context: {context}

        Question: {question}
        """

        self.prompt = PromptTemplate.from_template(self.template)


app = MyApp()


@app.post("/upload_document")
async def upload_document(request: Request):
    data = await request.json()
    file_path = data["file_path"]

    base_dir, filename = os.path.split(file_path)
    persist_directory = os.path.join(base_dir, "persist/directory", filename)

    # Check if the vector store already exists
    if os.path.exists(persist_directory):
        time.sleep(3)
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=app.embeddings)
    else:
        vectorstore = None

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Split the data into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(pages)

    if vectorstore is None:
        vectorstore = Chroma.from_documents(texts, embedding=app.embeddings, persist_directory=persist_directory)
    
    retriever = vectorstore.as_retriever()

    # Update the global retriever variable
    app.global_retriever = retriever

    return {"message": "Document uploaded successfully"}


@app.post("/invoke_model")
async def invoke_model(request: Request):
    
    data = await request.json()
    question = data["question"]

    chain = (
        {
            "context": itemgetter("question") | app.global_retriever,
            "question": itemgetter("question"),
        }
        | app.prompt
        | app.model
        | app.parser
    )
    answer = chain.invoke({"question": question})
    return answer

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
