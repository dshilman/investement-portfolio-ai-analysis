import os

from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, QuestionAnswerPrompt, download_loader


load_dotenv()
SimpleWebPageReader = download_loader("SimpleWebPageReader")

loader = SimpleWebPageReader()
documents = loader.load_data(urls=['https://testdriven.io/blog/django-custom-user-model/'])
index = GPTSimpleVectorIndex(documents)