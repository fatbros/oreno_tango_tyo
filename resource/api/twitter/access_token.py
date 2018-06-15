from flask_restful import Resource, reqparse, abort
from .twitter import Twitter
import oauth2 as oauth


class TwitterAccessToken(Resource, Twitter):
    parser = reqparse.RequestParser()
    parser.add_argument('oauth_token', type=str, required=True, help='oauth token of twitter')
    parser.add_argument('oauth_verifier', type=str, required=True, help='oauth verifier of twitter')

    def get_access_token(self, **kwargs):
        consumer = oauth.Consumer(key=kwargs['key'], secret=kwargs['secret'])
        token = oauth.Token(kwargs['oauth_token'], kwargs['oauth_verifier'])

        client = oauth.Client(consumer, token)
        resp, content = client.request(
            'https://api.twitter.com/oauth/access_token',
            'POST',
            body='oauth_verifier={0}'.format(kwargs['oauth_verifier'])
        )

        if(resp.status == 200):
            access_token = self.parse_qsl(content)

            # "oauth_token"
            # "oauth_token_secret"
            # "user_id"
            # "screen_name"
            return access_token

        else:
            abort(401, message=content.decode('utf-8'))

    def post(self):
        args = self.parser.parse_args()

        access_token = self.get_access_token(
            key=self.consumer_key,
            secret=self.consumer_secret,
            oauth_token=args.oauth_token,
            oauth_verifier=args.oauth_verifier
        )

        return access_token
