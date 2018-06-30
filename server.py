from flask import Flask
from flask_restful import Api

from resource.api.cards import Cards
from resource.api.google.credentials import GoogleAuthorizationUrl
from resource.api.google.credentials import GoogleCredentials
from resource.api.password.password import SavePassword
from resource.api.login.login import Login

import os

server_directory_path = os.path.dirname(os.path.abspath(__file__))

# flask setting
app = Flask(
    __name__,
    instance_relative_config=True,
    instance_path=os.path.join(server_directory_path, 'instance')
)
app.config.from_pyfile('config.py')

# flask_restful setting
api = Api(app)
api.add_resource(Cards, '/api/cards')
api.add_resource(GoogleAuthorizationUrl, '/api/google/authorization_url')
api.add_resource(GoogleCredentials, '/api/google/credentials')
api.add_resource(SavePassword, '/api/password')
api.add_resource(Login, '/api/login')


if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run(host=app.config['HOST'], port=app.config['PORT'])
