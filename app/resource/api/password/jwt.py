import jwt
import json
import base64
import os

jwt_config_file = open(
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '../../../instance/jwt.json'
    )
)

jwt_config = json.loads(jwt_config_file.read())
jwt_config_file.close()
jwt_secret = jwt_config['JWT_SECRET']


def verify(jwt_token):
    tmp = jwt_token.split('.')
    header = json.loads(base64.b64decode(tmp[0]).decode())

    try:
        if len(tmp) == 3 and header['alg'] == 'HS256':
            decode_data = jwt.decode(
                jwt_token, jwt_secret, algorithms=['HS256'])
            return decode_data
    except jwt.exceptions.InvalidSignatureError:
        return False
    except jwt.exceptions.DecodeError:
        return False

    return False


def createJwtToken(dict):
    jwt_token = jwt.encode(dict, jwt_secret, algorithm='HS256').decode('ascii')
    return jwt_token
