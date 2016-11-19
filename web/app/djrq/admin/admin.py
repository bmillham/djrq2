# encoding: utf-8

from ..templates.admin.admintemplate import page as _page
from ..templates.requests import requeststemplate

class Admin:
    __dispatch__ = 'resource'
    from .suggestions import Suggestions as suggestions
    from .mistags import Mistags as mistags

    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        if len(arg) > 0 and arg[0] != 'requests':
            return "Page not found: {}".format(arg[0])
        requestlist = self.queries.get_new_pending_requests()
        return requeststemplate(_page, "Admin", self._ctx, requestlist)
