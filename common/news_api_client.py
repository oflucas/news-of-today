import requests
from json import loads

NEWS_API_ENDPOINT = 'https://newsapi.org/v1/'
NEWS_API_KEY = '47e0c502179b4a7b8004154e6364ce1a'
ARTICLES_API = 'articles'
SORT_BY_TOP = 'top'

CNN = 'cnn'
DEFAULT_SOURCES = [CNN]

def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=ARTICLES_API):
    return end_point + api_name

def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {
            'apiKey': NEWS_API_KEY,
            'source': source,
            'sortBy': sortBy
        }
        response = requests.get(buildUrl(), params=payload)
        res_json = loads(response.content)

        # check res and extract info
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # put source info into each articles
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])
    return articles
