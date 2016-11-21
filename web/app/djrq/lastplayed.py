# encoding: utf-8

from .templates.lastplayed import lastplayedtemplate

class LastPlayed:
    __dispatch__ = 'resource'
    __resource__ = 'lastplayed'

    def __init__(self, context, *arg, **args):
        self._ctx = context
        self.queries = self._ctx.queries

    def get(self, *arg, **args):
        lplist = self.queries.get_last_played(count=self._ctx.lastplay_count)
        return lastplayedtemplate("{} Last Played".format(self._ctx.lastplay_count), self._ctx, lplist)
