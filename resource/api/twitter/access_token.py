from flask import current_app
from flask_restful import Resource, reqparse, abort
import oauth2 as oauth


def get_access_token(**kwargs):
    consumer = oauth.Consumer(key=kwargs['key'], secret=kwargs['secret'])
    token = oauth.Token(kwargs['oauth_token'], kwargs['oauth_verifier'])

    client = oauth.Client(consumer, token)
    resp, content = client.request(
        'https://api.twitter.com/oauth/access_token',
        'POST',
        body='oauth_verifier={0}'.format(kwargs['oauth_verifier'])
    )
    # bytesで返ってくるためstrに戻す
    decode_content = content.decode('utf-8')
    access_token = parse_qsl(decode_content)

    # "oauth_token"
    # "oauth_token_secret"
    # "user_id"
    # "screen_name"
    return access_token


def parse_qsl(url):
    param = {}
    for i in url.split('&'):
        _p = i.split('=')
        param.update({_p[0]: _p[1]})
    return param


class TwitterAccessToken(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('oauth_token', type=str, required=True, help='oauth token of twitter')
    parser.add_argument('oauth_verifier', type=str, required=True, help='oauth verifier of twitter')

    def post(self):
        args = self.parser.parse_args()

        config_list = current_app.config

        consumer_key = config_list['TWITTER_API_KEY']
        consumer_secret = config_list['TWITTER_API_SECRET']

        access_token = get_access_token(
            key=consumer_key,
            secret=consumer_secret,
            oauth_token=args.oauth_token,
            oauth_verifier=args.oauth_verifier
        )

        return access_token
