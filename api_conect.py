import requests

from log_config import setup_logger

logger = setup_logger(__name__)

def api_connecting(api_url):
    """

    A simple function that accepts a variable that is a url to the API.
    The function has the task of establishing a connection with the specified API.

    """
    try:
        response= requests.get(api_url,timeout=1800)
        if response.status_code == 400:
            logger.info("Bad Request: The server could not understand the request due to invalid syntax.")
        elif response.status_code == 401:
            logger.info("Unauthorized requests ")
        elif response.status_code == 500:
            logger.info("Internal Server Error: The server encountered an error while processing the request.")
        else:
            response.raise_for_status()

        return  response

    except requests.exceptions.ConnectTimeout:
        logger.info("Timeout requests")
    except requests.exceptions.ConnectionError:
        logger.info("Network problem (DNS failure, refused connection...")
    except requests.exceptions.URLRequired:
        logger.info("A valid URL is required to make a request.")
    except requests.exceptions.TooManyRedirects:
        logger.info("TooManyRedirects")