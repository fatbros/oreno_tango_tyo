from flask import current_app


class Twitter():
    def __init__(self):
        config_list = current_app.config

        self.consumer_key = config_list['TWITTER_API_KEY']
        self.consumer_secret = config_list['TWITTER_API_SECRET']
        self.callback_url = config_list['TWITTER_CALLBACK_URL']
        self.request_token_url = 'https://api.twitter.com/oauth/request_token'

    def parse_qsl(self, url):
        if(type(url) == bytes):
            url = url.decode('utf-8')

        param = {}
        for i in url.split('&'):
            _p = i.split('=')
            param.update({_p[0]: _p[1]})
        return param
