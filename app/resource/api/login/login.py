from flask_restful import Resource, reqparse, abort
from hashlib import sha256

from ...model.User import UserModel


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True,
                        help='password is required parameter')
    parser.add_argument('email', type=str, required=True,
                        help='email is required parameter')

    userModel = UserModel()

    def post(self):
        args = self.parser.parse_args()

        binary_password = args['password'].encode('UTF-8')
        hash_password = sha256(binary_password).hexdigest()

        get_user = Login.userModel.getUserFromPasswordAndEmail(
            hash_password,
            args.email
        )

        if get_user is None:
            abort(401)

        return {
            'objectid': str(get_user['_id']),
            'jwt_token': get_user['jwt_token'],
            'email': get_user['email']
        }
