import unittest
import copy
from resource.model.Model import Model


class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = Model()

    def test_formatMongoCursors(self):
        cards = self.model.db.cards.find()
        formatCards = self.model.formatMongoCursors(copy.deepcopy(cards))

        i = 0
        for card in cards:
            self.assertEqual(card['en_vo'], formatCards[i]['en_vo'])
            self.assertEqual(card['ja_vo'], formatCards[i]['ja_vo'])
            self.assertEqual(str(card['_id']), formatCards[i]['object_id'])
            i += 1


if __name__ == '__main__':
    unittest.main()
