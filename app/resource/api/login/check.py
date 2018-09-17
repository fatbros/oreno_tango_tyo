from flask_restful import Resource, reqparse, abort
from bson.objectid import ObjectId
from bson import errors

from ..password.jwt import verify


class Check(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('objectid', type=str, required=True,
                        help='objectid is required parameter')
    parser.add_argument('jwt_token', type=str, required=True,
                        help='jwt_token is required parameter')

    def post(self):
        args = self.parser.parse_args()

        try:
            ObjectId(args.objectid)
        except errors.InvalidId:
            return abort(403)

        verified_token = verify(args.jwt_token)
        if verified_token is False:
            return abort(403)

        if verified_token['objectid'] != args.objectid:
            return abort(403)

        return True
