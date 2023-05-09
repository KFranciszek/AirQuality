import requests

def api_connecting(api_url):
    """

    A simple function that accepts a variable that is a url to the API.
    The function has the task of establishing a connection with the specified API.

    """
    try:
        response= requests.get(api_url,timeout=1800)
        if response.status_code == 400:
            print("Bad Request: The server could not understand the request due to invalid syntax.")
        elif response.status_code == 401:
            print("Unauthorized requests ")
        elif response.status_code == 500:
            print("Internal Server Error: The server encountered an error while processing the request.")
        else:
            response.raise_for_status()

        return  response

    except requests.exceptions.ConnectTimeout:
        print("Timeout requests")
    except requests.exceptions.ConnectionError:
        print("Network problem (DNS failure, refused connection...")
    except requests.exceptions.URLRequired:
        print("A valid URL is required to make a request.")
    except requests.exceptions.TooManyRedirects:
        print("TooManyRedirects")