from flask_restful import Resource
from .twitter import Twitter
import oauth2 as oauth


class TwitterRequestToken(Resource, Twitter):
    def get_request_token(self, **kwargs):
        consumer = oauth.Consumer(key=kwargs['key'], secret=kwargs['secret'])
        client = oauth.Client(consumer)

        resp, content = client.request(
            '{0}?&oauth_callback={1}'.format(
                kwargs['request_token_url'],
                kwargs['callback_url']
            )
        )
        # bytesで返ってくるためstrに戻す
        decode_content = content.decode('utf-8')
        request_token = self.parse_qsl(decode_content)
        return request_token['oauth_token']

    def post(self):
        return self.get_request_token(
            key=self.consumer_key,
            secret=self.consumer_secret,
            request_token_url=self.request_token_url,
            callback_url=self.callback_url
        )
