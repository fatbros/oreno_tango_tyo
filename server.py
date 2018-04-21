from flask import Flask, render_template, session, redirect, url_for, request
from flask_restful import Resource, Api, reqparse, abort
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from pymongo import MongoClient, errors
from bson.json_util import dumps

import os

server_directory_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(
  __name__,
  instance_relative_config=True,
  instance_path=os.path.join(server_directory_path, 'instance')
)
app.config.from_pyfile('config.py')
api = Api(app)


blueprint = make_twitter_blueprint(
    api_key=app.config['TWITTER_API_KEY'],
    api_secret=app.config['TWITTER_API_SECRET']
)
app.register_blueprint(blueprint, url_prefix="/login")


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

api.add_resource(Cards, '/cards')


@app.route('/')
def index():
  for key in session.keys():
    print(key)
    print(session['twitter_oauth_token'])
    print(session['twitter_oauth_token']['user_id'])

  if not twitter.authorized:
    return redirect(url_for('twitter.login'))
  resp = twitter.get('account/settings.json')
  assert resp.ok
  return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])


@app.route('/logout')
def logout():
  session.clear()
  return 'clear session'


if __name__ == '__main__':
  app.debug = app.config['DEBUG']
  app.run(host=app.config['HOST'], port=app.config['PORT'])
