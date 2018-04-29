from .Model import Model
from flask_restful import abort


class CardModel(Model):
  def getAllCards(self, twitter_user_id):
    cards = self.db.cards.find({'twitter_user_id': twitter_user_id})
    return self.formateMongoCursors(cards)

  def insertCard(self, en_vo, ja_vo, twitter_user_id):
    # pymongo error handle document
    # http://api.mongodb.com/python/current/api/pymongo/errors.html
    try:
      inserted_card = self.db.cards.insert_one({
        'en_vo': en_vo,
        'ja_vo': ja_vo,
        'twitter_user_id': twitter_user_id
      })
    except:
      raise

    return inserted_card.acknowledged
