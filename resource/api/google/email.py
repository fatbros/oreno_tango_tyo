import google.oauth2.credentials
import googleapiclient.discovery


def get_userinfo_from_google(credentials_dict):
    credentials = google.oauth2.credentials.Credentials(
        **credentials_dict)

    people_service = googleapiclient.discovery.build(
        'people', 'v1', credentials=credentials)

    profile = people_service.people().get(
        resourceName='people/me',
        personFields='names,emailAddresses').execute()

    primary = [
        {
            'email': email['value'],
            'id': email['metadata']['source']['id']
        }
        for email in profile['emailAddresses']
        if 'primary' in email['metadata']
        and email['metadata']['primary'] is True
    ]

    return primary[0]
