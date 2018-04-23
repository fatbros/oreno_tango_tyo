from flask_restful import Resource, reqparse, abort
from pymongo import errors
from ..model.Cards import CardsModel


class Cards(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('en_vo', type=str, help='english vocabulary')
  parser.add_argument('ja_vo', type=str, help='japanese vocabulary')

  cards_model = CardsModel()

  def get(self):
    return Cards.cards_model.getAllCards()

  def post(self):
    args = self.parser.parse_args()

    if not args.en_vo or not args.ja_vo:
      abort(400, message='English vocabulary or japanese vocabulary is not specified')

    # pymongo error handle document
    # http://api.mongodb.com/python/current/api/pymongo/errors.html
    try:
      Cards.cards_model.insertCard(args.en_vo, args.ja_vo)
    except errors.DuplicateKeyError as e:
      abort(500, message='That vocabulary already exists')
    except e:
      print(e)
      abort(500)


  def delete(self):
    return {'hello': 'world by delete'}
