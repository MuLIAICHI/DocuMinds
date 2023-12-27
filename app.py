import streamlit as st
import boto3
import os
import io
from botocore.exceptions import NoCredentialsError
from llama_index import VectorStoreIndex
import docx2txt
import llama-cpp-python
from llama_index import StorageContext, load_index_from_storage

# AWS S3 Setup
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]
S3_BUCKET_NAME = st.secrets["S3_BUCKET_NAME"]
# Set up the OpenAI API key
api_key = st.secrets["API_KEY"]  # Replace with your OpenAI API key or use Streamlit secrets management

# Initialize S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket"""
    if object_name is None:
        object_name = file_name
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        st.error("Credentials not available for AWS S3.")
        return False
    return True

def download_from_s3(bucket, object_name, file_name):
    """Download a file from an S3 bucket"""
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except NoCredentialsError:
        st.error("Credentials not available for AWS S3.")
        return False
    return True

def process_uploaded_file(uploaded_file):
    try:
        if uploaded_file.name.endswith('.docx'):
            return docx2txt.process(io.BytesIO(uploaded_file.getvalue()))
        else:
            return uploaded_file.getvalue().decode()
    except Exception as e:
        st.error(f"Error processing file {uploaded_file.name}: {e}")
        return None

st.title("File Embedding App")

# File uploader
uploaded_files = st.file_uploader("Choose a text file", accept_multiple_files=True, type=['txt', 'docx'])

# User prompt input
user_prompt = st.text_input("Enter your prompt here:")

if st.button('Generate Response'):
    if uploaded_files and user_prompt:
        documents = [process_uploaded_file(uploaded_file) for uploaded_file in uploaded_files if uploaded_file is not None]
        
        if documents:
            try:
                # Local storage directory (for temporary use)
                storage_dir = "./storage"
                if not os.path.exists(storage_dir):
                    os.makedirs(storage_dir)

                # Create and persist the index
                index = VectorStoreIndex.from_documents(documents)
                storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
                index.storage_context.persist()

                # Upload the contents of the storage directory to S3
                for file_name in os.listdir(storage_dir):
                    full_path = os.path.join(storage_dir, file_name)
                    if os.path.isfile(full_path):
                        upload_to_s3(full_path, S3_BUCKET_NAME, file_name)

                # Load the index and create a query engine
                # Assuming the retrieval from S3 is handled within your querying logic
                index0 = load_index_from_storage(storage_context=storage_context)
                query_engine = index.as_query_engine()

                # Generate the response
                response = query_engine.query(user_prompt)

                # Display the response
                st.markdown(f"**Response:** {response}")
            except Exception as e:
                st.error(f"Error during processing and querying: {e}")
        else:
            st.error("No valid documents to process.")
    else:
        st.error("Please upload files and enter a prompt.")
