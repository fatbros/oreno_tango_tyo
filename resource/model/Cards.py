from .Model import Model
from flask_restful import abort


class FormateCard():
  def __init__(self, vo_data):
    self.en_vo = vo_data['en_vo']
    self.ja_vo = vo_data['ja_vo']

  def get(self):
    return {
      'en_vo': self.en_vo,
      'ja_vo': self.ja_vo
    }


def getFormatedCardsData(formated_cards):
  tmp = []
  for formated_card in formated_cards:
    tmp.append(formated_card.get())
  return tmp


class CardsModel(Model):
  def getAllCards(self, twitter_user_id):
    cards = self.db.cards.find({'twitter_user_id': twitter_user_id})

    formated_cards = []
    for card in cards:
      formated_cards.append(FormateCard(card))

    return getFormatedCardsData(formated_cards)

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
