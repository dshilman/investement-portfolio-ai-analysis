import argparse

import html2text
import requests
from dotenv import load_dotenv
from html2text import HTML2Text
from llama_index.core import Document, VectorStoreIndex

from app_config import config

load_dotenv()
def create_index(instruments: str):

    print('inside create_index()')
    articles = []
    for ticker in instruments.split(','):
        ticker_articles = get_stock_news_feed(ticker.strip())
        if len(ticker_articles) > 0:
            articles = articles + ticker_articles
    
    create_index_from_articles(articles)

    print('exiting create_index()')


def create_index_from_articles(data):

    print('inside create_index_from_articles()')

    h = HTML2Text()
    h.ignore_links = True
    h.ignore_emphasis = True

    documents = [Document(text = h.handle(t)) for t in data]

    index = VectorStoreIndex.from_documents(documents)
    path = "../indexed_files/api_index"

    index.storage_context.persist(persist_dir = f'./{path}')

    print('exiting create_index_from_articles()')


def get_stock_news_feed(ticker):

    print('inside get_news_feed(tickers)')

    querystring = {"symbol": ticker,"count":"21"}
    
    response = requests.get(config.NEWS_API_URL, headers=config.headers, params=querystring)

    articles = []

    if 'headlines' in response.json():
        news_feed = response.json()['headlines']
        
        for article in news_feed:
            summary = article['summary']
            if ticker in summary:                
                articles.append(summary)
    else:
        print(f"no articles for {ticker}")

    # print(articles)
    print('exiting get_news_feed(tickers)')

    return articles


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('instruments', type=str, help='must provide instruments e.g. "AAPL, IBM, TSLA, AMZN"')
    args = parser.parse_args()

    create_index(args.instruments)
