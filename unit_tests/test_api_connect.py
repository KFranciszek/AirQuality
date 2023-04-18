
import unittest
from unittest.mock import patch

class TestApiConnecting(unittest.TestCase):
    @patch('requests.get')
    def test_api_connecting_success(self, mock_get):
        # Przygotowanie atrapy obiektu Response
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.json = lambda: {"key": "value"}

        # Ustawienie atrapy, aby zwracała przygotowany obiekt Response
        mock_get.return_value = mock_response

        # Testowanie funkcji api_connecting z podmienionym obiektem requests.get
        api_url = "https://example.com/api/test"
        response = api_connecting(api_url)

        # Sprawdzenie, czy funkcja zwraca poprawną odpowiedź
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"key": "value"})

    @patch('requests.get')
    def test_api_connecting_exception(self, mock_get):
        # Ustawienie atrapy, aby rzuciła wyjątek RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Error message")

        # Testowanie funkcji api_connecting z podmienionym obiektem requests.get
        api_url = "https://example.com/api/test"

        with self.assertRaises(requests.exceptions.RequestException):
            api_connecting(api_url)

