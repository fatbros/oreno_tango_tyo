from flask_restful import Resource, reqparse, abort
from hashlib import sha256
from bson.objectid import ObjectId
from bson import errors

from ...model.User import UserModel


class SavePassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True,
                        help='password is required parameter')
    parser.add_argument('objectid', type=str, required=True,
                        help='objectid is required parameter')

    def post(self):
        args = self.parser.parse_args()

        try:
            objectid = ObjectId(args.objectid)
        except errors.InvalidId:
            return abort(403)

        binary_password = args['password'].encode('UTF-8')
        hash_password = sha256(binary_password).hexdigest()

        model = UserModel()
        update_password = model.updatePassword(objectid, hash_password)

        if update_password.acknowledged is True:
            return True

        else:
            return abort(403)
