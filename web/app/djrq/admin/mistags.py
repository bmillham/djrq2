# encoding: utf-8

from ..templates.admin.mistags import mistagstemplate
from web.ext.acl import when

@when(when.never)
class Mistags:
    __dispatch__ = 'resource'
    __resource__ = 'mistags'

    #from .common.get import get

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        return mistagstemplate("Mistags", self._ctx,  [])
