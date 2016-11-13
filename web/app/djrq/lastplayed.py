# encoding: utf-8

from .templates.lastplayed import lastplayedtemplate

class LastPlayed:
    __dispatch__ = 'resource'
    __resource__ = 'lastplayed'

    def __init__(self, context, *arg, **args):
        self._ctx = context
        self.queries = self._ctx.queries

    def get(self, *arg, **args):
        lplist = self.queries.get_last_played()
        if not self._ctx.session.username:
            self._ctx.session.username='someusername'
        else:
            print("Got a username from the session", self._ctx.session.username)
        return lastplayedtemplate("50 Last Played", self._ctx, lplist)
