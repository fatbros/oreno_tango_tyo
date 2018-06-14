from flask import current_app
from flask_restful import Resource, reqparse, abort
import oauth2 as oauth


def get_request_token(**kwargs):
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
    request_token = parse_qsl(decode_content)
    return request_token['oauth_token']


def parse_qsl(url):
    param = {}
    for i in url.split('&'):
        _p = i.split('=')
        param.update({_p[0]: _p[1]})
    return param


class TwitterRequestToken(Resource):

    # access_token_url = 'https://twitter.com/oauth/access_token'
    # authenticate_url = 'https://twitter.com/oauth/authorize

    def post(self):
        config_list = current_app.config

        consumer_key = config_list['TWITTER_API_KEY']
        consumer_secret = config_list['TWITTER_API_SECRET']
        callback_url = config_list['TWITTER_CALLBACK_URL']
        request_token_url = 'https://api.twitter.com/oauth/request_token'

        return get_request_token(
            key=consumer_key,
            secret=consumer_secret,
            request_token_url=request_token_url,
            callback_url=callback_url
        )
