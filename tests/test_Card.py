import unittest
from bson.objectid import ObjectId
from resource.model.Card import CardModel
from .config import twitter_user_id


class TestCardModel(unittest.TestCase):
    def setUp(self):
        self.cardModel = CardModel()

    def test_getAllCards(self):
        cards = self.cardModel.getAllCards(twitter_user_id)
        self.assertTrue(len(cards) > 0)

    def test_insertCard(self):
        insert_card = self.cardModel.insertCard(
            'en_vo', 'ja_vo', twitter_user_id)
        self.assertTrue(insert_card.acknowledged)

    def test_deleteCard(self):
        insert_card = self.cardModel.insertCard(
            'en_vo', 'ja_vo', twitter_user_id)

        self.cardModel.deleteCard(
            insert_card.inserted_id,
            twitter_user_id
        )

        deleted_card = self.cardModel.db.cards.find({
            '_id': ObjectId(insert_card.inserted_id)
        })

        self.assertEqual(deleted_card.count(), 0)
