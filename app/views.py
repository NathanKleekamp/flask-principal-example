# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, session, \
    make_response, current_app
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from flask.ext.principal import Identity, AnonymousIdentity, UserNeed, \
    RoleNeed, identity_loaded, identity_changed, Permission

from . import app, db, facebook
from .models import User, Role
from .facebook import GraphAPI


# Permissions
a = db.session.query(Role).filter(Role.name == 'admin').first()
admin_permission = Permission(RoleNeed(a.name))

e = db.session.query(Role).filter(Role.name == 'editor').first()
editor_permission = Permission(RoleNeed(e.name))


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
@login_required
def logout():
    logout_user()
    for key in ['identity.name', 'identity.auth_type']:
        session.pop(key, None)
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('index'))


@app.route('/test')
@login_required
def test():
    return render_template('test.html')


@app.route('/admin')
@login_required
@admin_permission.require()
def admin():
    print(current_user)
    return 'You are an admin'


@app.route('/login/authorized', methods=['GET'])
@facebook.authorized_handler
def facebook_authorized(response):
    if response is None:
        # In a real case, this should return error message/description
        return redirect(url_for('index'))

    next = request.args.get('next')
    token = response['access_token']

    me = GraphAPI.me(token).json()

    user = User.get_or_create(me['id'], me['name'], me['email'])

    if not user.is_active():
        return 'Your account has been deactivated. Contact the admin for it \
                to be reinstated.'

    login_user(user, remember=True)

    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.id))

    if next:
        return redirect(next)

    return redirect(url_for('index'))


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

    identity.user = current_user

    print('on_identity_loaded: ', identity.provides)
    print('on_identity_loaded: ', current_user)
    print('on_identity_loaded: ', identity)
