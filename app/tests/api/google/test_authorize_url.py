import unittest
from server import app
import json


class TestGoogleAuthorizeUrl(unittest.TestCase):
    api_url = '/api/google/authorization_url'

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_success(self):
        data = self.app.get(TestGoogleAuthorizeUrl.api_url)
        self.assertEqual(data.status_code, 200)

        dict_data = json.loads(data.get_data())

        self.assertGreater(len(dict_data['authorization_url']), 0)
        self.assertGreater(len(dict_data['state']), 0)
