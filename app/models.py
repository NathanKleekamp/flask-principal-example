# -*- coding: utf-8 -*-

import hashlib

from uuid import uuid4

from . import db, login_serializer


def md5(data):
    return hashlib.md5(data).hexdigest()


def uuid_gen():
    '''Used to generate random UUID for user'''
    return str(uuid4().hex)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Don't expose UUID to public or it will defeat the encrypted cookie for
    # Flask-Login
    uuid = db.Column(db.String(34), nullable=False, unique=True,
                     default=uuid_gen)
    fb_id = db.Column(db.BigInteger, nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, fb_id, name, email):
        self.fb_id = fb_id
        self.name = name
        self.email = email

    def __repr__(self):
        return '< User: {0} >'.format(self.name)

    def is_authenticated(self):
        '''Required by Flask-Login'''
        return True

    def is_active(self):
        '''Required by Flask-Login'''
        return self.active

    def is_anonymous(self):
        '''Required by Flask-Login'''
        return False

    def get_id(self):
        '''Required by Flask-Login'''
        return unicode(self.fb_id)

    def get_auth_token(self):
        '''
        Create secure token to store in cookie for secure Flask-Login
        Remember Me functionality.

        See http://goo.gl/UvhIgI and http://goo.gl/niOYDQ
        '''
        data = [str(self.fb_id), md5(self.uuid)]
        return login_serializer.dumps(data)

    @staticmethod
    def get_or_create(fb_id, name, email):
        user = User.query.filter_by(fb_id=fb_id).first()
        if user is None:
            user = User(fb_id, name, email)
            db.session.add(user)
            db.session.commit()
        return user
