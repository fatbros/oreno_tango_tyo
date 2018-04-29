from flask import session
from flask_restful import Resource, reqparse, abort
from pymongo import errors
from ..model.Card import CardModel
from ..model.User import UserModel


def get_twitter_user_id(func):
  def _wrapper(*args, **kwargs):
    try:
      return func(*args, session['twitter_oauth_token']['user_id'], **kwargs)
    except KeyError:
      abort(403)

  return _wrapper


class Cards(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('en_vo', type=str, help='english vocabulary')
  parser.add_argument('ja_vo', type=str, help='japanese vocabulary')

  card_model = CardModel()

  @get_twitter_user_id
  def get(self, twitter_user_id):
    return Cards.card_model.getAllCards(twitter_user_id)

  @get_twitter_user_id
  def post(self, twitter_user_id):
    args = self.parser.parse_args()

    if not args.en_vo or not args.ja_vo:
      abort(400, message='English vocabulary or japanese vocabulary is not specified')

    try:
      Cards.card_model.insertCard(args.en_vo, args.ja_vo, twitter_user_id)
    except:
      abort(500)
