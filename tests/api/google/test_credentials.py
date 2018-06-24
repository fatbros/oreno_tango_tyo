import unittest
from unittest.mock import patch
from server import app
import json
from bson.objectid import ObjectId

from resource.model.User import UserModel


class CredentialsMock():
    def __init__(self):
        pass

    @property
    def token(self):
        return 'Credentials.token'

    @property
    def refresh_token(self):
        return 'Credentials.refresh_token'

    @property
    def token_uri(self):
        return 'Credentials.token_uri'

    @property
    def client_id(self):
        return 'Credentials.client_id'

    @property
    def client_secret(self):
        return 'Credentials.client_secret'

    @property
    def scopes(self):
        return 'Credentials.scopes'


class FlowMock():
    def __init__(self):
        self._redirect_uri = None
        self.test = 'test'

    @property
    def redirect_uri(self):
        return self._redirect_uri

    @redirect_uri.setter
    def redirect_uri(self, uri):
        self._redirect_uri = uri

    def fetch_token(self, **kwargs):
        self.credentials = CredentialsMock()


class TestGoogleCredentials(unittest.TestCase):
    api_url = '/api/google/credentials'

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_post_when_parameters_isnt_set(self):
        data = self.app.post(TestGoogleCredentials.api_url)
        self.assertEqual(data.status_code, 400)

        data = self.app.post(TestGoogleCredentials.api_url, data={
            'callback_url': 'aaa'
        })
        self.assertEqual(data.status_code, 400)

        data = self.app.post(TestGoogleCredentials.api_url, data={
            'state': 'bbb'
        })
        self.assertEqual(data.status_code, 400)

    def test_post_when_invalid_parameter(self):
        data = self.app.post(TestGoogleCredentials.api_url, data={
            'callback_url': 'http://localhost:5000/',
            'state': 'bbb'
        })
        self.assertEqual(data.status_code, 400)

        data = self.app.post(TestGoogleCredentials.api_url, data={
            'callback_url': 'https://localhost:5000/',
            'state': 'bbb'
        })
        self.assertEqual(data.status_code, 400)

    @patch('google_auth_oauthlib.flow.Flow.from_client_config')
    @patch('resource.api.google.credentials.get_userinfo_from_google')
    def test_post_success(self, mock_get_userinfo, mock_flow):
        mock_flow.return_value = FlowMock()
        mock_get_userinfo.return_value = {
            'email': 'test@gmail.com',
            'id': '1000'
        }

        data = self.app.post(TestGoogleCredentials.api_url, data={
            'callback_url': 'https://localhost:5000/success_using_mock',
            'state': 'bbb'
        })

        self.assertEqual(data.status_code, 200)

        dict_data = json.loads(data.get_data())
        objectid = ObjectId(dict_data['objectid'])
        user = UserModel()
        user_data = user.getUser(objectid)

        correct_keys = [
            '_id', 'token', 'refresh_token', 'token_uri',
            'client_id', 'client_secret', 'scopes', 'email', 'id'
        ]

        for index, value in enumerate(user_data):
            data = user_data[value]
            self.assertTrue(value in correct_keys)

            if type(data) is ObjectId:
                data = str(data)

            self.assertGreater(len(data), 0)
