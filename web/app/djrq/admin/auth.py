# encoding: utf-8

from ..templates.admin.auth import authtemplate
from web.ext.acl import when

@when(when.always, inherit=False)
class Auth:
    __dispatch__ = 'resource'
    __resource__ = 'auth'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        return authtemplate("Suggestions", self._ctx,  [])

    def lookup(self):
        print('lookup called')
        return True

    def authenticate(self, context, identifier, credential):
        print('authenticate session', context.session.usertheme)
        print('authenticate called', dir(context.session), identifier, credential)
        return [True, 'bmillham']
