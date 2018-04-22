from flask import Blueprint, session, flash, redirect, url_for

app = Blueprint('logout', __name__)

@app.route('/')
def index():
  session.clear()
  flash(message='session clear')
  return redirect(url_for('index.index'))
