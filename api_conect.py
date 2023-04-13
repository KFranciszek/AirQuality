import requests
import json
import sqlite3

def api_connecting(api_url):
    try:
        response = requests.get(api_url)
        return  response
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
