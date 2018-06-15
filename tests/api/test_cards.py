import unittest
import json
from server import app
from tests.config import twitter_user_id


class TestApiCards(unittest.TestCase):
    api_url = '/api/cards'

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        self.pop_userid_session()

    def set_userid_session(self, user_id):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['twitter_oauth_token'] = {
                    'user_id': user_id
                }

    def pop_userid_session(self):
        with self.app as client:
            with client.session_transaction() as sess:
                if sess.get('twitter_oauth_token'):
                    sess.pop('twitter_oauth_token')

    def test_get_when_session_isnt_set(self):
        data = self.app.get(TestApiCards.api_url)
        self.assertEqual(data.status_code, 403)

    def test_get_unknow_user(self):
        self.set_userid_session(1111)
        data = self.app.get(TestApiCards.api_url)

        json_list = json.loads(data.get_data())
        self.assertEqual(len(json_list), 0)

    def test_get_success(self):
        self.set_userid_session(twitter_user_id)
        data = self.app.get(TestApiCards.api_url)
        self.assertEqual(data.status_code, 200)

        json_list = json.loads(data.get_data())
        self.assertGreater(len(json_list), 0)

    def test_post_when_session_isnt_set(self):
        data = self.app.post(TestApiCards.api_url)
        self.assertEqual(data.status_code, 403)

    def test_post_when_data_isnt_set(self):
        self.set_userid_session(twitter_user_id)
        data = self.app.post(TestApiCards.api_url)
        self.assertEqual(data.status_code, 400)

        data = self.app.post(TestApiCards.api_url, data={
            'en_vo': 'en'
        })
        self.assertEqual(data.status_code, 400)

        data = self.app.post(TestApiCards.api_url, data={
            'ja_vo': 'ja'
        })
        self.assertEqual(data.status_code, 400)

    def test_post_success(self):
        self.set_userid_session(twitter_user_id)

        data = self.app.post(TestApiCards.api_url, data={
            'en_vo': 'en',
            'ja_vo': 'ja'
        })
        json_list = json.loads(data.get_data())

        self.assertTrue(json_list['acknowledged'])

    def test_delete_when_session_isnt_set(self):
        data = self.app.delete(TestApiCards.api_url)
        self.assertEqual(data.status_code, 403)

    def test_delete_invalid_objectid(self):
        self.set_userid_session(twitter_user_id)

        data = self.app.delete(TestApiCards.api_url, data={
            'object_id': '111111111111'
        })
        self.assertEqual(data.status_code, 400)

        data = self.app.delete(TestApiCards.api_url, data={
            'object_id': 'xxxxxxxxxxxxxxxxxxxxxxxx'
        })
        self.assertEqual(data.status_code, 400)

    def test_delete_success(self):
        self.set_userid_session(twitter_user_id)

        post_data = self.app.post(TestApiCards.api_url, data={
            'en_vo': 'en',
            'ja_vo': 'ja'
        })
        json_list_by_post = json.loads(post_data.get_data())

        delete_data = self.app.delete(TestApiCards.api_url, data={
            'object_id': json_list_by_post['insert_id']
        })
        json_list_by_delete = json.loads(delete_data.get_data())
        self.assertTrue(json_list_by_delete['acknowledged'])

        delete_data = self.app.delete(TestApiCards.api_url, data={
            'object_id': json_list_by_post['insert_id']
        })
