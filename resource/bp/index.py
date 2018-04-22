from flask import Blueprint, url_for, session, render_template, current_app
from flask_dance.contrib.twitter import twitter

app = Blueprint('index', __name__)

@app.route('/')
def index():
  if not twitter.authorized:
    return render_template('index.html',
      login_url=url_for('twitter.login')
    )
  else:
    resp = twitter.get('account/settings.json')
    assert resp.ok

    parsed=resp.json()

    return render_template('index.html',
      logout_url=url_for('logout.index'),
      screen_name=parsed['screen_name'],
      is_admin=int(session['twitter_oauth_token']['user_id']) == current_app.config['ADMIN_ID']
    )
