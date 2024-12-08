import http.client
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')


def get_fgi():
    """
    Fetches data on the Fear and Greed Index from the RapidAPI endpoint.

    This function connects to the Fear and Greed Index API hosted on RapidAPI, 
    retrieves the data, and returns the raw response in JSON format.

    Returns:
        bytes: The raw JSON response from the API 

    Notes:
        - Requires the RapidAPI key to be set as an environment variable (`RAPID_API_KEY`).
        - Ensure the `.env` file in the parent directory contains the API key.
    """

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
