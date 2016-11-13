# encoding: utf-8

from .templates.siteoptions import siteoptionstemplate


class SiteOptions:
    __dispatch__ = 'resource'
    __resource__ = 'siteoptions'


    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context

    def get(self, *arg, **args):
        return siteoptionstemplate("Site Options", self._ctx)

    def post(self, *arg, **args):
        self._ctx.session.usertheme = args['theme']
        return siteoptionstemplate("Site Options", self._ctx, updated=True)
