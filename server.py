from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
api = Api(app)

class Cards(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('en_vo', type=str, help='english vocabulary')
  parser.add_argument('ja_vo', type=str, help='japanese vocabulary')

  def get(self):
    client = MongoClient('localhost', 27017)
    db = client['vo_book']
    cards = db.cards.find()
    return dumps(cards)

  def post(self):
    args = self.parser.parse_args()
    client = MongoClient('localhost', 27017)
    db = client['vo_book']
    inserted_card = db.cards.insert_one({
      'en_vo': args.en_vo,
      'ja_vo': args.ja_vo
    })
    return inserted_card.acknowledged

  def delete(self):
    return {'hello': 'world by delete'}

api.add_resource(Cards, '/cards')

@app.route('/')
def hello():
  return render_template('index.html')

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=5000)
