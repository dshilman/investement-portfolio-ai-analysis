from flask import Flask, request, render_template, jsonify
import os
from pathlib import Path
import logging
from dotenv import load_dotenv
from llama_index import VectorStoreIndex, ServiceContext, Document
import requests


app = Flask(__name__)


# Load the index from disk
load_dotenv()

index = None

# set up the index, either load it from disk to create it on the fly


def load_data(portfolio):

    print('inside load_data()')

    url = "https://mboum-finance.p.rapidapi.com/qu/quote"

    querystring = {"symbol": portfolio}

    headers = {
        "X-RapidAPI-Key": "cc0fa5785dmshe4af69ddd9fbcc6p16321fjsn145f158f15b5",
        "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
    }

    print('calling quote API')
    response = requests.get(url, headers=headers, params=querystring)

    securities = response.json
    print(f'response {securities}')

    contextArray = []

    print('looping thru response')

    for security in securities:
        company = security['shortName']
        symbol = security['symbol']
        asset_class = security['quoteType']

        news_feed = get_news_feed(symbol)

        secDict = {'company name': company, 'security cusip': symbol,
                   'security asset class': asset_class, 'news feed': news_feed}

        contextArray.append(secDict)

    print('exiting load_data')

    return contextArray


def get_news_feed(symbol):

    print('inside get_news_feed')

    url = "https://mboum-finance.p.rapidapi.com/ne/news/"

    querystring = {"symbol": symbol}

    headers = {
        "X-RapidAPI-Key": "cc0fa5785dmshe4af69ddd9fbcc6p16321fjsn145f158f15b5",
        "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
    }

    print ('calling get news API')
    response = requests.get(url, headers=headers, params=querystring)

    news_feed = response.json['item']

    print ('API response')


    articles = []
    for article in news_feed:
        articles.append(article['description'])

    print ('exiting get_news_feed')

    return articles


def create_index(portfolio: str, contextArray):

    global index

    print ("inside create_index")

    stocks = portfolio.split(',')

    portfolio_text = f"My invetsment portfolion has {len(stocks)} stocks {portfolio}"
    context_documents_dict = {"portfolio": [Document(portfolio_text)]}
    docs = []
    doc = Document().from_dict(context_documents_dict)
    docs.append(doc)

    for context in contextArray:
        context_doc = Document().from_dict(context)
        docs.append(context_doc)

    index = VectorStoreIndex.from_documents(documents=docs)

    print ("exiting create_index")


def initialise_index():
    portfolio = {"aapl, ibm, amzn"}
    dataContext = load_data(portfolio=portfolio)

    create_index(portfolio=portfolio, contextArray=dataContext)


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
        answer = index.query(query_str)
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'answer': e})

    return jsonify({'answer': answer.response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
