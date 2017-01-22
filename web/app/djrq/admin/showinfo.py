# encoding: utf-8

from ..templates.admin.showinfo import showinfotemplate
import datetime
import pytz

class ShowInfo:
    __dispatch__ = 'resource'
    __resource__ = 'showinfo'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        so = self.queries.get_siteoptions()
        return showinfotemplate("Show Information", self._ctx,  showinfo=so)

    def post(self, *arg, **args):
        if args['show_time'] != '':
            dt = datetime.datetime.strptime(args['show_time'], '%Y-%m-%d %H:%M %z')
            args['show_time'] = dt.astimezone(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M %z')
        result = self.queries.save_siteoptions(**args)
        so = self.queries.get_siteoptions()
        return showinfotemplate("Show Information Saved", self._ctx,  showinfo=so, saved=True)
