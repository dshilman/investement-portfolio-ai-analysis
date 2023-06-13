import os
from dotenv import load_dotenv
from llama_index import VectorStoreIndex, SimpleDirectoryReader

data_source = "data"

load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
print("loadind data")
documents = SimpleDirectoryReader(f'{data_source}.md').load_data()
print("creating index")
index = VectorStoreIndex(documents)
print("saving index")
index.save_to_disk(f'./index_files/index_{data_source}.json')
print("index saved")
