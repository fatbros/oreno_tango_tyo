import jwt
import json
import base64
from ..read_file import get_jwt_secret
jwt_secret = get_jwt_secret()


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

    return False
