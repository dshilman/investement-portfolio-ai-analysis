import os
from datetime import datetime, timedelta

import pytz
import requests
from dotenv import load_dotenv
from llama_index import Document, StorageContext, VectorStoreIndex
from llama_index.node_parser.simple import SimpleNodeParser

load_dotenv()


def create_index():

    print('inside create_index()')

    tickers = "AAPL, IBM, TSLA, AMZN"
    articles = get_stock_news_feed(tickers)
    create_index_from_articles(articles=articles)

    print('exiting create_index()')


def create_index_from_articles(articles):

    print('inside create_index_from_articles()')

    path = "indexed_files/api_index"

    documents = []
    for article in articles:
        documents.append(Document(article))

    nodes = SimpleNodeParser().get_nodes_from_documents(documents)

    index = VectorStoreIndex(nodes)
    index.storage_context.persist(f'./{path}')

    print('exiting create_index_from_articles()')


def get_stock_news_feed(tickers):

    print('inside get_news_feed(tickers)')

    url = os.environ.get('NEWS_API_URL')

    querystring = {"symbol": tickers}

    headers = {
        "X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
        "X-RapidAPI-Host": os.environ.get('X-RapidAPI-Host')
    }
    response = requests.get(url, headers=headers, params=querystring)

    news_feed = response.json()['item']

    # print(f"Market News API response for {tickers}:")
    # print(json.dumps(news_feed, indent=2))

    date_format = "%b-%d-%y %I:%M %p"
    est = pytz.timezone('US/Eastern')

    articles = []
    for article in news_feed:
        # pub_date = article['pubDate']
        datetime_utc = datetime.strptime(
            article['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
        est_datetime = datetime_utc.astimezone(tz=est)

        title = article['title']
        link = article['link']
        description = article['description']
        document = f"""Article Title: {title}
        Published Date: {est_datetime.strftime(date_format)}
        Article Description: {description}
        Source: {link}"""

        articles.append(document)

    # print(articles)
    print('exiting get_news_feed(tickers)')

    return articles


if __name__ == '__main__':
    create_index()
