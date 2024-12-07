# Python 3
import http.client
import urllib.parse
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

# Rewrite this function with some other packages that I am more familiar with


def get_news(ticker: str, stock_name: str):

    conn = http.client.HTTPSConnection('api.thenewsapi.com')

    time_frame = (datetime.now() - timedelta(weeks=30)).strftime("%Y-%m")
    print(time_frame)

    params = urllib.parse.urlencode({
        'api_token': os.getenv('THE_NEWS_API_KEY'),
        'language': 'en',
        'limit': 3,  # is the default limit provided by the news API
        # Sorting by API provided relevance score for search criteria
        'sort': 'relevance_score',
        'published_after': time_frame,
    })

    conn.request('GET', '/v1/news/all?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    print(data.decode('utf-8'))


get_news('AAPL', 'Apple')
