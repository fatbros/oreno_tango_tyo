import unittest
import json
from server import app


class TestTwitterRequestToken(unittest.TestCase):
    api_url = '/api/v1/auth/twitter_request_token'

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_post_success(self):
        data = self.app.post('/api/v1/auth/twitter_request_token')
        self.assertEqual(data.status_code, 200)

        request_token = json.loads(data.get_data())
        self.assertEqual(type(request_token), str)
        self.assertGreater(len(request_token), 0)
