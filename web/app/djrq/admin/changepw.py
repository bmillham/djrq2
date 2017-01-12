# encoding: utf-8

from ..templates.admin.auth import authtemplate, change_pw_template
from .auth import Auth
from web.ext.acl import when
from webob.exc import HTTPFound
import hashlib
import scrypt
from os import urandom

@when(when.matches(True, 'session.authenticated', True), when.never)
class ChangePassword:
    __dispatch__ = 'resource'
    __resource__ = 'changepw'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        return change_pw_template("Change Password", self._ctx)

    def post(self, *arg, **args):
        r, res = Auth.authenticate(self._ctx, identifier=self._ctx.session.username, credential=args['currentpw'])
        if r == True:
            spw = scrypt.encrypt(str(urandom(64)), args['newpw'], maxtime=0.5)
            #add_spw = Users.__table__.update().where(Users.uname == args.admin_user).values(spword=spw)
            res.spword = spw
            self._ctx.db.commit()
            self._ctx.response = HTTPFound(location='/admin')

        return change_pw_template("Change Password", self._ctx,  status_message='Current Password Incorrect.')

