# encoding: utf-8

from ..templates.admin.mistags import mistagstemplate
from web.ext.acl import when

class Mistags:
    __dispatch__ = 'resource'
    __resource__ = 'mistags'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        print(self._ctx.session.authenticated)
        return mistagstemplate("Mistags", self._ctx,  [])
