import json
import os

import requests
from dotenv import load_dotenv
from llama_index import SimpleWebPageReader, VectorStoreIndex

load_dotenv()


def create_index():

    tickers = "AAPL, IBM, TSLA, AMZN"
    article_links = get_stock_news_feed(tickers)
    create_index_from_web(article_links=article_links)

def create_index_from_web(article_links):

    path = "indexed_files"
    data_source = "web_index"

    documents = SimpleWebPageReader().load_data(urls=article_links)
    index = VectorStoreIndex(documents)
    index.save_to_disk(f'./{path}/index_{data_source}.json')

def get_stock_news_feed(tickers):

    print('inside get_news_feed')

    url = os.environ.get('NEWS_API_URL')

    querystring = {"symbol": tickers}

    headers = {
        "X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
        "X-RapidAPI-Host": os.environ.get('X-RapidAPI-Host')
    }
    response = requests.get(url, headers=headers, params=querystring)

    news_feed = response.json()['item']

    print(f"Market News API response for {tickers}:")
    print(json.dumps(news_feed, indent=2))

    articles = []
    for article in news_feed:
        articles.append(article['link'])

    print('exiting get_news_feed')

    return articles


if __name__ == '__main__':
    create_index()