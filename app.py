from flask import Flask, request, render_template, jsonify
import os
from pathlib import Path
import logging
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader


app = Flask(__name__)


# Load the index from disk
load_dotenv()

index = None

# set up the index, either load it from disk to create it on the fly
def initialise_index():
    global index

    index_file = os.getenv("INDEX_FILE", "./index_files/index.json")
    index_folder = os.getenv("LOAD_DIR", "./index_files")

    file = Path(index_file)
    print (f"file {file.name} exists: {file.exists}")

    folder = Path(index_folder)
    print (f"folder {folder.name} exists: {(folder.exists)}")

    # if index_file and os.path.exists(index_file) and os.path.isfile(index_file):
    if file.exists:
        index = GPTSimpleVectorIndex.load_from_disk(index_file)
    elif folder.exists:
        documents = SimpleDirectoryReader(index_folder).load_data()
        index = GPTSimpleVectorIndex().build_index_from_documents(documents=documents)
    else:
        raise Exception ("Missing index loction")

    logging.debug ("Index Created")

initialise_index()

@app.route('/')
def home():
   return render_template('index.html')


@app.route("/api/query")
def query():
    global index

    query_str = request.args.get('question', None)
    print (f"question: {query_str}")
    if not query_str:
        return jsonify({"error": "Please provide a question."})

    answer = None
    try:
        answer = index.query(query_str)
    except Exception as e:
        print (f"Exception: {e}")
        return jsonify({'answer': e})

    return jsonify({'answer': answer.response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

