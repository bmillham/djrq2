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
        stats_info = {
                      'total_artists': self.queries.get_total_artists(),
                      'total_albums': self.queries.get_total_albums(),
                      'total_played_by_me': self.queries.get_total_played_by_me(),
                      'top_10_artists': self.queries.get_top_10(),
                      '10 Most Requested': self.queries.get_top_requested(),
                      'Top 10 Requestors': self.queries.get_top_requestors(),
                      '10 Most Played By Me': self.queries.get_top_played_by(played_by_me=True),
                      '10 Most Played By Other DJs': self.queries.get_top_played_by(played_by_me=False),
                      '10 Most Played By All DJs': self.queries.get_top_played_by(played_by_me='all'),
                     }

        return statstemplate("Library Statistics", self._ctx, stats_info)
