# encoding: utf-8

from ..templates.admin.auth import authtemplate, change_pw_template
from web.ext.acl import when
from webob.exc import HTTPFound
import hashlib
import scrypt

@when(when.always, inherit=False)
class Auth:
    __dispatch__ = 'resource'
    __resource__ = 'auth'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        if 'logout' in args:
            self._ctx.deauthenticate(self._ctx)

        return authtemplate("Login", self._ctx,  [])

    def post(self, *arg, **args):
        r = self._ctx.authenticate(self._ctx, identifier=args['username'], credential=args['password'])
        if r:
            self._ctx.session.username = args['username']
            # Check if the spword field is empty. If so, force a password change
            try:
                result = self._ctx.db.query(self._ctx.Users.spword).filter(self._ctx.Users.uname == args['username']).one()
            except:
                return authtemplate("Login", self._ctx, [])
            if result.spword == '' or result.spword is None:
                return change_pw_template('Change Password', self._ctx, first_access=True)
            else:
                self._ctx.response = HTTPFound(location='/admin')
        if args['username'] == 'changepw':
            self._ctx.response = HTTPFound(location='/admin/changepw')
        return authtemplate("Login", self._ctx,  [])

    def lookup(self):
        return True

    def authenticate(context, identifier=None, credential=None):
        try:
            res = context.db.query(context.Users).\
                filter(context.Users.uname == identifier).one()
        except:
            print(f'Unable to authenticate {identifier}')
            return False, False

        if res.spword == '' or res.spword is None: # If spword is not defined, use the old site password
            print('Using old site password')
            if res.pword == hashlib.md5(credential.encode()).hexdigest():
                result = True
            else:
                result = False
        else:
            try:
                y = scrypt.decrypt(res.spword, credential, maxtime=1.0)
                result = True
            except scrypt.error:
                result = False

        return [result, res]
