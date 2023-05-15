
import unittest
import  requests
from api_conect import api_connecting


class TestApiConnecting(unittest.TestCase):

    def test_valid_api_url(self):
        api_url  = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
        result_test = api_connecting(api_url)
        self.assertEqual(result_test.status_code, 200)

    def test_unvalid_api_url(self):
        api_url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAlll'
        with self.assertRaises(requests.exceptions.HTTPError):
            api_connecting(api_url)

if __name__ == '__main__':
    unittest.main()
