# encoding: utf-8

from ..templates.admin.botoptions import botoptionstemplate

class BotOptions:
    __dispatch__ = 'resource'
    __resource__ = 'botoptions'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        so = self.queries.get_siteoptions()
        return botoptionstemplate("Bot Options", self._ctx,  siteoptions=so)

    def post(self, *arg, **args):
        result = self.queries.save_siteoptions(**args)
        so = self.queries.get_siteoptions()
        return botoptionstemplate("Bot Options Saved", self._ctx,  siteoptions=so, saved=True)
