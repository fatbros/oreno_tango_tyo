from .Model import Model
from bson.objectid import ObjectId

# pymongo error handle document
# http://api.mongodb.com/python/current/api/pymongo/errors.html


class CardModel(Model):
    def getAllCards(self, twitter_user_id):
        cards = self.db.cards.find({'twitter_user_id': twitter_user_id})
        return self.formatMongoCursors(cards)

    def insertCard(self, en_vo, ja_vo, twitter_user_id):
        inserted_card = self.db.cards.insert_one({
            'en_vo': en_vo,
            'ja_vo': ja_vo,
            'twitter_user_id': twitter_user_id
        })

        return inserted_card

    def deleteCard(self, object_id, twitter_user_id):
        delete_card = self.db.cards.delete_one({
            '_id': ObjectId(object_id),
            'twitter_user_id': twitter_user_id
        })

        return delete_card
