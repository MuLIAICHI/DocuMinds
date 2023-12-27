# DocuMinds - File Embedding App

DocuMinds is a Streamlit-based web application designed to process and analyze text documents. It allows users to upload documents, input a prompt, and receive insightful responses based on the content of the uploaded documents.

## Features

- Upload multiple text documents in `.txt` or `.docx` format.
- Enter a textual prompt for querying the uploaded documents.
- Process documents to create embeddings stored in AWS S3.
- Generate and display responses based on user prompts.

## Development and Deployment Process

### 1. Local Development

- Write the Streamlit application script in Python.
- Test the application locally to ensure all functionalities (uploading, processing, querying, displaying results) work correctly.

### 2. AWS S3 Setup

- Create an AWS account and set up an S3 bucket for storing the application data.
- Obtain AWS Access Key ID and Secret Access Key for programmatic access.

### 3. AWS S3 Integration

- Integrate AWS S3 with the Streamlit app using the `boto3` Python library.
- Implement functions to handle data upload and retrieval with S3.

### 4. Preparing for Deployment

- Create a GitHub repository for the app.
- Include a `requirements.txt` file for dependencies.
- Use `.gitignore` to exclude sensitive files from the repository.

### 5. Deployment on Streamlit Cloud

- Set up a Streamlit Cloud account and link it to GitHub.
- Configure AWS credentials and other secrets in Streamlit Cloud’s settings.
- Deploy the app by connecting to the GitHub repository.

### 6. Post-Deployment Testing

- Verify the deployed app’s functionality and integration with AWS S3.
- Test file uploading, prompt processing, and response generation.

### 7. Monitoring and Maintenance

- Regularly monitor the app’s performance.
- Update and redeploy as needed for maintenance or new features.

## Usage

Visit the deployed Streamlit app URL. Upload text documents, enter a prompt, and receive generated responses based on the content of your documents.

## Contributions

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](link-to-issues-page) if you want to contribute.

## Author

- LIAICHI MUSTAPHA aka MuLIAICHI
