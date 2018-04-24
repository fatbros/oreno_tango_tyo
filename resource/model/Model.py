from pymongo import MongoClient, errors


class Model():
  mongo_host = 'localhost'
  mongo_port = 27017

  def __init__(self):
    client = MongoClient(Model.mongo_host, Model.mongo_port)
    self.db = client['vo_book']
    self.errors = errors
