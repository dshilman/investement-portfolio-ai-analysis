from flask import Flask, request, render_template, jsonify
import os
from pathlib import Path
import logging
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext, Document
import requests
import json

app = Flask(__name__)


# Load the index from disk
# load_dotenv()

index = None
headers = {
        "X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
        "X-RapidAPI-Host": os.environ.get('X-RapidAPI-Host')
    }
# set up the index, either load it from disk to create it on the fly


def load_data(portfolio):

    print('inside load_data()')

    url = os.environ.get('QUOTE_API_URL')

    querystring = {"symbol": portfolio}

    print('calling quote API')
    response = requests.get(url, headers=headers, params=querystring)

    securities = response.json()
    print(f'response {securities}')

    securities_array = []

    print('looping thru response')

    for security in securities:
        company = security['shortName']
        symbol = security['symbol']
        asset_class = security['quoteType']

        news_feed = get_news_feed(symbol)

        secDict = {'company name': company, 'security cusip': symbol,
                   'security asset class': asset_class, 'news feed': news_feed}

        securities_array.append(secDict)

    print('exiting load_data')

    return securities_array


def get_news_feed(symbol):

    print('inside get_news_feed')

    url = os.environ.get('NEWS_API_URL')

    querystring = {"symbol": symbol}

    print('calling get news API')
    response = requests.get(url, headers=headers, params=querystring)

    news_feed = response.json()['item']

    print('API response')

    articles = []
    for article in news_feed:
        articles.append(article['description'])

    print('exiting get_news_feed')

    return articles


def create_index(portfolio: str, securities):

    global index

    print("inside create_index")

    for security in securities:
        symbol = security['security cusip']
        company_name = security['company name']
        stock_asset_class = security['security asset class']
        news_feed = security['news feed']

        f = open(f"data/{symbol}.txt", "a")
        f.write(f"I have {symbol} stock in my investement portfolio\n")
        f.write(f"Company Name is {company_name}\n")
        f.write(f"Stock asset class is {stock_asset_class}\n")

        news_feed_s = "\n".join(news_feed)
        f.write("Company news feed:\n")
        f.write(news_feed_s)

        f.close()

    print("creating index")

    documents = SimpleDirectoryReader('data').load_data()
    index = VectorStoreIndex.from_documents(documents)

    print("exiting create_index")


def initialise_index():
    portfolio = "aapl, ibm, amzn"
    data = load_data(portfolio=portfolio)
    create_index(portfolio=portfolio, securities=data)


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

    answer = None
    try:
        query_engine = index.as_query_engine()
        answer = query_engine.query(query_str)
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'answer': e})

    return jsonify({'answer': answer.response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, load_dotenv=True)
