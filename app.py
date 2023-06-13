import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from llama_index import SimpleDirectoryReader, VectorStoreIndex

app = Flask(__name__)


# Load the index from disk
# load_dotenv()

index = None
headers = {
    "X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
    "X-RapidAPI-Host": os.environ.get('X-RapidAPI-Host')
}
# set up the index, either load it from disk to create it on the fly


def load_stock_data(portfolio):

    print('inside load_data()')

    url = os.environ.get('QUOTE_API_URL')

    querystring = {"symbol": portfolio}

    print('calling quote API')
    response = requests.get(url, headers=headers, params=querystring)

    securities = response.json()

    print('Quote API response:')
    print(json.dumps(securities, indent=2))

    securities_array = []

    print('looping thru response')

    for security in securities:
        company = security['shortName']
        symbol = security['symbol']
        asset_class = security['quoteType']

        print (f'Calling market news API for {symbol}')
        news_feed = get_stock_news_feed(symbol)

        secDict = {'company name': company, 'security cusip': symbol,
                   'security asset class': asset_class, 'news feed': news_feed}

        securities_array.append(secDict)

    print('exiting load_data')

    return securities_array


def get_stock_news_feed(symbol):

    print('inside get_news_feed')

    url = os.environ.get('NEWS_API_URL')

    querystring = {"symbol": symbol}

    response = requests.get(url, headers=headers, params=querystring)

    news_feed = response.json()['item']

    print(f"Market News API response for {symbol}:")
    print(json.dumps(news_feed, indent=2))

    articles = []
    for article in news_feed:
        articles.append(article['description'])

    print('exiting get_news_feed')

    return articles


def create_data_files(securities):

    print("inside create_data_files")

    for security in securities:
        create_data_file(security=security)

    print("exiting create_data_files")

def create_data_file(security: dict):
        
    symbol = security['security cusip']
    company_name = security['company name']
    stock_asset_class = security['security asset class']
    news_feed = security['news feed']

    f = open(f"data/{symbol}.txt", "a")
    f.write(f"I have {symbol} stock in my investement portfolio\n")
    f.write(f"Company Name is {company_name}\n")
    f.write(f"Stock asset class is {stock_asset_class}\n")

    news_feed_s = "\n\n".join(news_feed)
    f.write("Company news feed:\n")
    f.write(news_feed_s)

    f.close()

def create_index():

    global index

    print("inside create_index")
    documents = SimpleDirectoryReader('data').load_data()
    index = VectorStoreIndex.from_documents(documents)
    print("existing create_index")

def initialise_index():
    portfolio = "aapl"
    data = load_stock_data(portfolio=portfolio)
    create_data_files(securities=data)
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
