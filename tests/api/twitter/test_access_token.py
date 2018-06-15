import unittest
from server import app


class TestTwitterAccessToken(unittest.TestCase):
    api_url = '/api/v1/auth/twitter_access_token'

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_post_when_parameters_isnt_set(self):
        data = self.app.post(TestTwitterAccessToken.api_url)
        self.assertEqual(data.status_code, 400)

        data = self.app.post(TestTwitterAccessToken.api_url, data={
            'oauth_token': ''
        })
        self.assertEqual(data.status_code, 400)

        data = self.app.post(TestTwitterAccessToken.api_url, data={
            'oauth_verifier': ''
        })
        self.assertEqual(data.status_code, 400)

    def test_post_when_invalid_parameters(self):
        data = self.app.post(TestTwitterAccessToken.api_url, data={
            'oauth_token': 'aaaaaa',
            'oauth_verifier': 'bbbbb'
        })

        self.assertEqual(data.status_code, 401)

    # TODO 正常系のTEST
    # @mock.patch('', side_effect=mocked_client_request)
    # def test_post_success(self):
