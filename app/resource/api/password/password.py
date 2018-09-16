from flask_restful import Resource, reqparse, abort
from hashlib import sha256
from bson.objectid import ObjectId
from bson import errors

from ...model.User import UserModel
from .jwt import verify


class Password(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True,
                        help='password is required parameter')
    parser.add_argument('objectid', type=str, required=True,
                        help='objectid is required parameter')
    parser.add_argument('jwt_token', type=str, required=True,
                        help='jwt_token is required parameter')

    def put(self):
        args = self.parser.parse_args()

        try:
            objectid = ObjectId(args.objectid)
        except errors.InvalidId:
            return abort(403)

        verified_token = verify(args.jwt_token)
        if verified_token is False:
            return abort(403)

        if verified_token['objectid'] != args.objectid:
            return abort(403)

        binary_password = args['password'].encode('UTF-8')
        hash_password = sha256(binary_password).hexdigest()

        model = UserModel()
        update_password = model.updatePassword(objectid, hash_password)

        if update_password.acknowledged is True:
            return True

        else:
            return abort(403)
