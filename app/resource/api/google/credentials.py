from flask_restful import Resource, reqparse, abort
import google_auth_oauthlib.flow
from oauthlib.oauth2.rfc6749 import errors
import os
import json

server_directory_path = os.path.dirname(os.path.abspath(__file__))
client_secrets_path = os.path.join(
    server_directory_path, '../../../', 'instance/client_secret.json')
scopes = ['https://www.googleapis.com/auth/user.emails.read',
          'https://www.googleapis.com/auth/plus.login']


def _read_client_secrets():
    secrets_file = open(client_secrets_path, 'r')
    return json.load(secrets_file)


class GoogleAuthorizationUrl(Resource):
    def get(self):
        secrets_file = _read_client_secrets()

        # Use the client_secret.json file
        # to identify the application requesting
        # authorization. The client ID (from that file) and
        # access scopes are required.
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            secrets_file,
            scopes=scopes)

        # Indicate where the API server will redirect
        # the user after the user completes
        # the authorization flow. The redirect URI is required.
        flow.redirect_uri = secrets_file['web']['redirect_uris'][0]

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that
            # you can refresh an access token without
            # re-prompting the user for permission.
            # Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization.
            # Recommended as a best practice.
            include_granted_scopes='true')

        return {
            'authorization_url': authorization_url,
            'state': state
        }


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


from .email import get_userinfo_from_google
from ...model.User import UserModel


class GoogleCredentials(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('callback_url', type=str, required=True,
                        help='callback_url is required parameter')
    parser.add_argument('state', type=str, required=True,
                        help='state is required parameter')

    def post(self):
        args = self.parser.parse_args()
        secrets_file = _read_client_secrets()

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            secrets_file,
            scopes=scopes,
            state=args.state)

        flow.redirect_uri = secrets_file['web']['redirect_uris'][0]

        # Use the authorization server's
        # response to fetch the OAuth 2.0 tokens.
        authorization_response = args.callback_url

        try:
            flow.fetch_token(authorization_response=authorization_response)

        except (
            # callback_urlがhttpsでない場合
            errors.InsecureTransportError,
            # callback_url, stateが不正の場合
            errors.MissingCodeError,
            # stateデータが不正の場合
            errors.MismatchingStateError,
            # 承認後, 同じcallback_url, stateでリクエスト
            errors.InvalidGrantError
        ):
            return abort(400)

        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        credentials = flow.credentials
        credentials_dict = credentials_to_dict(credentials)

        # save credentials, userinfo
        userinfo = get_userinfo_from_google(credentials_dict)
        credentials_dict['email'] = userinfo['email']
        credentials_dict['id'] = userinfo['id']

        insert_data = UserModel().insertUser(credentials_dict)

        return {
            'objectid': str(insert_data.inserted_id),
            'email': userinfo['email']
        }
