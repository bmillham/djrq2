# encoding: utf-8

from web.ext.acl import when
from ..templates.admin.admintemplate import page as _page
from ..templates.requests import requeststemplate

@when(when.matches(True, 'session.authenticated', True))
class Logout:
    __dispatch__ = 'resource'

    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        self._ctx.deauthenticate(self._ctx)
