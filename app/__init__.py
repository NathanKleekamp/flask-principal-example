# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.principal import Principal
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauth import OAuth


app = Flask(__name__)
app.config.from_object('app.conf.Config')
db = SQLAlchemy(app)


oauth = OAuth()

#Setting up Facebook remote application for Flask-Oauth
facebook = oauth.remote_app('facebook',
    base_url = 'https://graph.facebook.com/',
    request_token_url = None,
    access_token_url = '/oauth/access_token',
    authorize_url = 'https://www.facebook.com/dialog/oauth',
    consumer_key = app.config['FACEBOOK_CONSUMER_KEY'],
    consumer_secret = app.config['FACEBOOK_CONSUMER_SECRET'],
    request_token_params = {'scope': 'email, manage_pages'}
)


from . import models, views
from .core import get_login_manager, get_principals

get_login_manager(app)

# Activate Principal Extension
principals = get_principals(app)

@app.before_first_request
def mk_db():
    db.create_all()
