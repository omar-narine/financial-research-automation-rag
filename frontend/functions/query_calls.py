import requests


def query_rag(query):
    url = "http://127.0.0.1:5000/query"
    params = {"query": query}
    response = requests.get(url, json=params)

    print(response.json())
