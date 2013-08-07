# -*- coding: utf-8 -*-

import os

from datetime import timedelta


class Config(object):
    DEBUG = True
    TESTING = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
    FACEBOOK_CONSUMER_KEY = os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_CONSUMER_SECRET = os.environ.get('FACEBOOK_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REMEMBER_COOKIE_DURATION = timedelta(days=360)
