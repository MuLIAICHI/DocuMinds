from flask import Flask, request, render_template, jsonify
import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, template_folder='static/templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        query = data['query']
        response = process_query(query)
        response_data = [{'text': node.get_text()} for node in response]
        return response_data
    return render_template('index.html')

def process_query(query):
    print("Received query:", query)  # Add this line to print the query to the console
    if not os.path.exists('data'):
        os.makedirs('data')
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
    if not os.path.exists('./storage'):
        os.makedirs('./storage')
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index0 = load_index_from_storage(storage_context=storage_context)
    query_engine = index0.as_query_engine()
    response = query_engine.query(query)
    return response



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get port from env variable or default to 5000
    app.run(host='0.0.0.0', port=port)
