# encoding: utf-8

from .templates.whatsnew import whatsnewtemplate


class WhatsNew:
    __dispatch__ = 'resource'
    __resource__ = 'whatsnew'


    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        newlist = self.queries.get_new_artists(days=self._ctx.whatsnewdays)
        return whatsnewtemplate("Whats New", self._ctx, self._ctx.whatsnewdays, newlist)
