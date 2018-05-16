from pymongo import MongoClient, errors


class Model():
    mongo_host = 'localhost'
    mongo_port = 27017

    def __init__(self):
        client = MongoClient(Model.mongo_host, Model.mongo_port)
        self.db = client['vo_book']
        self.errors = errors

    def formatMongoCursors(self, cursors):
        formatedCards = []
        for cursor in cursors:
            formatedCards.append({
                'en_vo': cursor['en_vo'],
                'ja_vo': cursor['ja_vo'],
                'object_id': str(cursor['_id'])
            })

        return formatedCards
