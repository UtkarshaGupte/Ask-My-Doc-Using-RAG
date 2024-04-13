# Ask-my-doc-using-RAG

## Running the Frontend:

To run the frontend of the AskMyDoc application, follow these steps:

1. Ensure you have Python installed on your system.
2. Install the required dependencies by running the following command in your terminal or command prompt:
 ` pip install streamlit aiohttp `
3. Navigate to the directory containing the frontend file in your terminal or command prompt.
4. Run the Streamlit application by executing the following command:
` streamlit run ask_my_doc_frontend.py `
5. Once the application is running, you can access it by opening a web browser and visiting the URL provided in the terminal output (usually http://localhost:8501).

## Running the Backend:

To run the backend of the AskMyDoc application, follow these steps:

1. Ensure you have Python installed on your system.
2. Install the required dependencies by running the following command in your terminal or command prompt: ` pip install langchain pypdf docarray uvicorn fastapi `
3. Navigate to the directory containing the backend file in your terminal or command prompt.
4. Run the FastAPI application using the uvicorn server by executing the following command: ` uvicorn ask_my_doc_backend:app --reload `
5. Once the backend server is running, it will listen for requests on http://localhost:8888 by default.
6. Ensure that the frontend is configured to send requests to the correct backend URL (e.g., http://localhost:8888).

With both the frontend and backend running, you can now upload documents, ask questions related to the document's content, and receive answers through the user-friendly interface provided by the Streamlit application.

