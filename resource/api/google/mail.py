from flask import current_app
from flask_restful import Resource
import google.oauth2.credentials
import googleapiclient.discovery


class GooglePeopleEmail(Resource):
    def get(self):
        credentials = google.oauth2.credentials.Credentials(
            **current_app.config['TEST_CREDENTIALS'])

        people_service = googleapiclient.discovery.build(
            'people', 'v1', credentials=credentials)

        profile = people_service.people().get(
            resourceName='people/me',
            personFields='names,emailAddresses').execute()

        primary = [email['value'] for email in profile['emailAddresses']
                   if 'primary' in email['metadata'] and
                   email['metadata']['primary'] is True]

        return primary[0]
