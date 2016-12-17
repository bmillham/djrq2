# encoding: utf-8

from .templates.stats import statstemplate

class Stats:
    __dispatch__ = 'resource'
    __resource__ = 'stats'


    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context
        self.queries = self._ctx.queries

    def get(self, *arg, **args):
        if 'topartists' in args:
            return statstemplate("Top Artists", self._ctx, topartists=args['topartists'])
        """ To speed up page loading, do the DB access in the template """
        return statstemplate("Library Statistics", self._ctx)
