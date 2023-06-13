import os

from dotenv import load_dotenv
from llama_index import VectorStoreIndex, download_loader


load_dotenv()

urls = []
data_source = None

SimpleWebPageReader = download_loader("SimpleWebPageReader")

loader = SimpleWebPageReader()
documents = loader.load_data(urls=urls)
index = VectorStoreIndex(documents)
index.save_to_disk(f'./index_files/index_{data_source}.json')
