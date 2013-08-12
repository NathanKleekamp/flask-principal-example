# -*- coding: utf-8 -*-

from flask.ext.login import LoginManager, AnonymousUserMixin, current_user
from flask.ext.principal import Principal, Identity

from werkzeug.datastructures import ImmutableList

from . import app
from .models import User
from .utils import md5, login_serializer


class AnonymousUser(AnonymousUserMixin):
    """AnonymousUser definition"""

    def __init__(self):
        self.roles = ImmutableList()

    def has_role(self, *args):
        """Returns `False`"""
        return False


def load_user(fb_id):
    return User.query.filter_by(fb_id=fb_id).first()


def load_token(token):
    '''
    Load the secure token. See http://goo.gl/UvhIgI and http://goo.gl/niOYDQ
    '''
    # This allows us to enforce the exipry date of the token server side and
    # not rely on the users cookie to exipre.
    try:
        max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
        data = login_serializer.loads(token, max_age=max_age)
        user = User.query.filter_by(fb_id=data[0]).first()

        if user and md5(user.uuid) == data[1]:
            return user
    except:
        pass
    return AnonymousUser()


def get_login_manager(app):
    lm = LoginManager(app)
    lm.session_protection = 'strong'
    lm.anonymous_user = AnonymousUser
    lm.login_view = '/login'
    lm.user_loader(load_user)
    lm.token_loader(load_token)
    lm.init_app(app)
    return lm


def load_identity():
    if not isinstance(current_user._get_current_object(), AnonymousUser):
        identity = Identity(current_user.id)
        return identity


def get_principals(app):
    p = Principal(app)
    p.identity_loader(load_identity)
    return p
