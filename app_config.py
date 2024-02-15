import os

class config():
    NEWS_API_URL = "https://fidelity-investments.p.rapidapi.com/news/list-by-symbol"

   
    OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
    RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
    RapidAPI_Host = "fidelity-investments.p.rapidapi.com"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RapidAPI_Host
    }
