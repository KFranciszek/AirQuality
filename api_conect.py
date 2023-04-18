import requests
import json
import sqlite3

def api_connecting(api_url):
    """

    A simple function that accepts a variable that is an url to the API.
    The function has the task of establishing a connection with the specified API.

    """
    try:
        response = requests.get(api_url)
        return  response
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
