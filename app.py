import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from llama_index import (SimpleDirectoryReader, StorageContext,
                         VectorStoreIndex, load_index_from_storage)

app = Flask(__name__)


# Load the index from disk
# load_dotenv()

index = None


def create_index():

    global index

    storage_context = StorageContext.from_defaults(
        persist_dir="./indexed_files/api_index")
    index = load_index_from_storage(storage_context)

    print("existing create_index")


def initialise_index():
    # portfolio = "aapl, amzn, ibm, tsla"
    # data = load_stock_data(portfolio=portfolio)
    # create_data_files(securities=data)
    create_index()


initialise_index()


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/api/query")
def query():
    global index

    query_str = request.args.get('question', None)
    print(f"question: {query_str}")
    if not query_str:
        return jsonify({"error": "Please provide a question."})

    response = None
    try:

        query_engine = index.as_query_engine()
        response = query_engine.query(query_str).response

    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'response': e})

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, load_dotenv=True)
