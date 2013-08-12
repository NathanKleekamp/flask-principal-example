# -*- coding: utf-8 -*-

from . import db
from .utils import md5, uuid4, login_serializer


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Don't expose UUID to public or it will defeat the encrypted cookie for
    # Flask-Login
    uuid = db.Column(db.String(34), nullable=False, unique=True,
                     default=uuid4)
    fb_id = db.Column(db.BigInteger, nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean, nullable=False, default=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, fb_id, name, email):
        self.fb_id = fb_id
        self.name = name
        self.email = email

    def __repr__(self):
        return '< User: {0} >'.format(self.name)

    def is_active(self):
        '''Required by Flask-Login'''
        return self.active

    def is_authenticated(self):
        '''Required by Flask-Login'''
        return True

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


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '< Role: {0} >'.format(self.name)
