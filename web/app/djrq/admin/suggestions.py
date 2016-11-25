# encoding: utf-8

from ..templates.admin.suggestions import suggestionstemplate

class Suggestions:
    __dispatch__ = 'resource'
    __resource__ = 'suggestions'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        return suggestionstemplate("Suggestions", self._ctx,  [])
