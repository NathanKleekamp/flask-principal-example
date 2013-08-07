# -*- coding: utf-8 -*-

import requests

from . import app

app_id = app.config['FACEBOOK_CONSUMER_KEY']
app_secret = app.config['FACEBOOK_CONSUMER_SECRET']


class GraphAPI(object):
    base_url = 'https://graph.facebook.com/{0}/'

    def __init__(self, token):
        self.token = token

    def query(self, fb_id='me', **kwargs):
        url = self.base_url.format(fb_id)
        params = {'access_token': self.token}
        params = dict(params.items() + kwargs.items())
        r = requests.get(url, params=params)
        return r

    @staticmethod
    def me(token):
        graph = GraphAPI(token)
        query = graph.query()
        return query
