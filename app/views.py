# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request
from flask.ext.login import login_user, logout_user, current_user, \
    login_required  # , fresh_login_required

from . import app, facebook, login_manager, login_serializer
from .models import User, md5
from .facebook import GraphAPI


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    return facebook.authorize(callback=url_for('facebook_authorized',
                              next=request.args.get('next') or request.referrer
                              or None, _external=True))


@app.route('/logout')
@login_required  # logout() should always have this decorator from Flask-Login
def logout():
    # Tell Flask-Login the user's been logged out.
    logout_user()
    return redirect(url_for('index'))


@app.route('/test')
#@fresh_login_required  # See http://goo.gl/to0oEL
@login_required
def test():
    return render_template('test.html')


@app.route('/login/authorized', methods=['GET'])
@facebook.authorized_handler
def facebook_authorized(response):
    '''
    Get's Oauth token and User's info from Facebook, Flask-
    Login logs in the user, and redirects to proper location.
    '''
    if response is None:
        # In a real case, this should return error message/description
        return redirect(url_for('index'))

    next = request.args.get('next')
    token = response['access_token']

    # Get identity from Facebook Graph
    me = GraphAPI.me(token).json()

    # Get or create the user
    user = User.get_or_create(me['id'], me['name'], me['email'])

    # Login with Flask-Login
    login_user(user, remember=True)

    if next:
        return redirect(next)

    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(fb_id):
    '''
    This needs to return the user or None as required by Flask-Login
    '''
    return User.query.filter_by(fb_id=fb_id).first()


@login_manager.token_loader
def load_token(token):
    '''
    Load the secure token. See http://goo.gl/UvhIgI and http://goo.gl/niOYDQ
    '''
    # This allows us to enforce the exipry date of the token server side and
    # not rely on the users cookie to exipre.
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()

    # Decrypt the Security Token
    data = login_serializer.loads(token, max_age=max_age)

    # Locate the User
    user = User.query.filter_by(fb_id=data[0]).first()

    if user and md5(user.uuid) == data[1]:
        return user
    return None
