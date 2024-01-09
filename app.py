import os
import requests
from flask import Flask, request, render_template
import cloudinary
from llama_index.llms import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cloudinary configuration
cloudinary.config_from_url(os.getenv('CLOUDINARY_URL'))

app = Flask(__name__)

def download_file_from_cloudinary(public_id, folder):
    """Download a file from Cloudinary and save it locally."""
    file_url = cloudinary.CloudinaryImage(public_id).build_url(resource_type='raw')
    local_filename = os.path.join(folder, public_id.split('/')[-1])

    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

def setup_local_data_folder():
    """Ensure the data folder exists and is populated with the latest files from Cloudinary."""
    if not os.path.exists('data'):
        os.makedirs('data')

    # List of public IDs for your PDFs in Cloudinary
    pdf_public_ids = ['r2yncmiyext8kznryls9', 'xlkkivfuq1740pryafnm', 'yrg4aqvgu4xrf1zs2bk9', 'xlkkivfuq1740pryafnm','sblvwf3yxaepbjpwt8yv','vgapxh3nwtrcgsgoisd1','fse5ibcerh9ynuwxblqo','vsavfk8rhdgwlixko2bz','wr1dm4mwkv7nwjpnelyx','zpk1hl0yv1mqxo2ewe1o','txvsa645dpj08ocxoj9z' ]  # Replace with actual public IDs

    for public_id in pdf_public_ids:
        download_file_from_cloudinary(public_id, 'data')

@app.before_first_request
def initialize_app():
    setup_local_data_folder()
    # Any other initialization logic can go here

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        response = process_query(query)
        return render_template('response.html', response=response)
    return render_template('index.html')

def process_query(query):
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index0 = load_index_from_storage(storage_context=storage_context)
    query_engine = index0.as_query_engine()
    response = query_engine.query(query)
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get port from env variable or default to 5000
    app.run(host='0.0.0.0', port=port)
