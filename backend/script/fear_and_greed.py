import http.client
import json
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')

# FUNCTION NEEDS TO PROVIDE PROPER RESPONSE BACK TO THE API CALL


def get_fgi():

    conn = http.client.HTTPSConnection("fear-and-greed-index.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': os.getenv("RAPID_API_KEY"),
        'x-rapidapi-host': "fear-and-greed-index.p.rapidapi.com"
    }

    conn.request("GET", "/v1/fgi", headers=headers)

    res = conn.getresponse()
    data = res.read()

    # Returning the repsonse JSON from the API request with all data to be decoded as necessary
    return data
