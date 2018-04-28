from flask import Blueprint, url_for, session, render_template, current_app, g
from flask_dance.contrib.twitter import twitter

from ..model.User import UserModel

app = Blueprint('index', __name__)

@app.route('/')
def index():
  if not twitter.authorized:
    return render_template('index.html',
      login_url=url_for('twitter.login')
    )
  else:
    user_model = UserModel()
    user_id = session['twitter_oauth_token']['user_id']
    user_data = user_model.getUser(user_id)

    # register of first time
    if not user_data:
      resp = twitter.get('account/settings.json')
      assert resp.ok

      parsed=resp.json()
      admin = int(session['twitter_oauth_token']['user_id']) == current_app.config['ADMIN_ID']

      # adjust the data to insert in to database
      parsed['admin'] = admin
      parsed['twitter_user_id'] = session['twitter_oauth_token']['user_id']

      screen_name = parsed['screen_name']

      user_model.insertUser(parsed)
      # retrieve and substitute the inserted user data
      user_data = user_model.getUser(user_id)

    return render_template('index.html',
      logout_url=url_for('logout.index'),
      screen_name=user_data['screen_name'],
      admin=user_data['admin']
    )
