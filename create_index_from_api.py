import os

import requests
from dotenv import load_dotenv
from llama_index import Document, StorageContext, VectorStoreIndex
from llama_index.node_parser.simple import SimpleNodeParser

load_dotenv()


def create_index():

    tickers = "AAPL, IBM, TSLA, AMZN"
    articles = get_stock_news_feed(tickers)
    create_index_from_articles(articles=articles)


def create_index_from_articles(articles):

    path = "indexed_files"
    data_source = "api_index"

    documents = []
    for article in articles:
        documents.append(Document(article))

    nodes = SimpleNodeParser().get_nodes_from_documents(documents)

    index = VectorStoreIndex(nodes)
    index.storage_context.persist(f'./{path}/{data_source}')


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
    # print(json.dumps(news_feed, indent=2))

    articles = []
    for article in news_feed:
        articles.append(article['description'])

    print('exiting get_news_feed')

    return articles


if __name__ == '__main__':
    create_index()
