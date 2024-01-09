from flask import Flask, request, render_template
import os
from llama_index.llms import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


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
