import streamlit as st
import asyncio
import aiohttp
import os

# Set page config
st.set_page_config(page_title="AskMyDoc", page_icon=":speech_balloon:")

# CSS styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F2F6;
        padding: 2rem;
        border-radius: 1rem;
    }
    h1, h2 {
        color: #4A5568;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

async def main():

    # Header and description
    st.header("Unleashing Knowledge from Documents")
    st.write("Upload a document and ask your question to get an answer.")

    # Upload document
    with st.container():
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if st.button("Upload"):
            if uploaded_file is not None:
                with st.spinner("Uploading your document..."):
                    message = await upload_document(uploaded_file)

                    if message:
                        st.success("Document uploaded successfully!")                               
                    else:
                        st.error("Error uploading document.")


    st.empty()

    # Ask question and get answer
    with st.form("question_form"):
        question = st.text_input("Ask your question:")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if uploaded_file is not None:
                with st.spinner("Getting answer..."):
                    answer = await get_answer(question)
                    st.write(f"{answer}")
            else:
                st.error("Please upload a document first.")


async def upload_document(uploaded_file):
   
    # Send the file contents and question to the backend
    backend_upload_url = "http://127.0.0.1:8000/upload_document"

    try:
        # Get the current working directory   
        cwd = os.getcwd()

        # Create the file path
        file_path = os.path.join(cwd, uploaded_file.name)

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            contents = uploaded_file.read()
            buffer.write(contents)

        data = {"file_path": file_path}

        async with aiohttp.ClientSession() as session:
            async with session.post(backend_upload_url, json=data) as response:
                if response.status == 200:
                    msg = await response.json()
                    return msg
                else:
                    return "Error: Could not upload document. Status code: {}".format(response.status)

    except aiohttp.ClientError as e:
        return f"Error: {e}"



async def get_answer(question):

    # Send the file contents and question to the backend
    backend_answer_retrieval_url = "http://127.0.0.1:8000/invoke_model"

    data = { "question": question}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(backend_answer_retrieval_url, json=data) as response:
                if response.status == 200:
                    answer = await response.json()
                    return answer
                else:
                    return "Error: Could not retrieve answer from the backend. Status code: {}".format(response.status)

    except aiohttp.ClientError as e:
        return f"Error: {e}"

if __name__ == "__main__":
    asyncio.run(main())