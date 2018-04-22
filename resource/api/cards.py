from flask_restful import Resource, reqparse, abort
from pymongo import MongoClient, errors


class FormateCard():
  def __init__(self, vo_data):
    self.en_vo = vo_data['en_vo']
    self.ja_vo = vo_data['ja_vo']

  def get(self):
    return {
      'en_vo': self.en_vo,
      'ja_vo': self.ja_vo
    }


def getFormatedCardsData(formatedCards):
  tmp = []
  for formatedCard in formatedCards:
    tmp.append(formatedCard.get())
  return tmp


class Cards(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('en_vo', type=str, help='english vocabulary')
  parser.add_argument('ja_vo', type=str, help='japanese vocabulary')

  def get(self):
    client = MongoClient('localhost', 27017)
    db = client['vo_book']
    cards = db.cards.find()

    formatedCards = []
    for card in cards:
      formatedCards.append(FormateCard(card))

    return getFormatedCardsData(formatedCards)

  def post(self):
    args = self.parser.parse_args()

    if not args.en_vo or not args.ja_vo:
      abort(400, message='English vocabulary or japanese vocabulary is not specified')

    client = MongoClient('localhost', 27017)
    db = client['vo_book']

    # pymongo error handle document
    # http://api.mongodb.com/python/current/api/pymongo/errors.html
    try:
      inserted_card = db.cards.insert_one({
        'en_vo': args.en_vo,
        'ja_vo': args.ja_vo
      })
    except errors.DuplicateKeyError as e:
      abort(500, message='That vocabulary already exists')
    except:
      return False

    return inserted_card.acknowledged

  def delete(self):
    return {'hello': 'world by delete'}
