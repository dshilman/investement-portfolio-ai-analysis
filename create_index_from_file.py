import os
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader

data_source = "data"

load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
print("loadind data")
documents = SimpleDirectoryReader(f'{data_source}').load_data()
print("creating index")
index = GPTSimpleVectorIndex(documents)
print("saving index")
index.save_to_disk(f'./index_files/{data_source}.json')
print("index saved")
