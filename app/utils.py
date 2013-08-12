# -*- coding: utf-8 -*-

import hashlib
import uuid

from itsdangerous import URLSafeTimedSerializer

from . import app


login_serializer = URLSafeTimedSerializer(app.config.get('SECRET_KEY'))


def md5(data):
    return hashlib.md5(data).hexdigest()


def uuid4():
    '''Used to generate random UUID for user'''
    return str(uuid.uuid4().hex)
