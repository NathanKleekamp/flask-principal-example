# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_oauth import OAuth
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
app.config.from_object('app.conf.Config')

db = SQLAlchemy(app)


# Setting up the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

# Where to redirect users when encountering a @login_required view
login_manager.login_view = '/login'  # Has to be an absolute/relative URL

# Login_serializer used to encryt and decrypt the cookie token for the remember
# me option of Flask-Login
login_serializer = URLSafeTimedSerializer(app.config.get('SECRET_KEY'))


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


@app.before_first_request
def mk_db():
    db.create_all()
