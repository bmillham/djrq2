# encoding: utf-8

from ..templates.admin.auth import authtemplate
from web.ext.acl import when
from webob.exc import HTTPFound

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
        if r == True:
            self._ctx.response = HTTPFound(location='/admin')
        return authtemplate("Login", self._ctx,  [])

"""    def lookup(self):
        print('lookup called')
        return True

    def authenticate(self, context, identifier=None, credential=None):
        print('authenticate session', context.session.usertheme)
        print('authenticate called', dir(context.session), identifier, credential)
        result = self.queries.verify_user(identifier, credential)
        print('verify user:', result)
        return [True, 'bmillham']"""
