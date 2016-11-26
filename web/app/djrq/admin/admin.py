# encoding: utf-8

from web.ext.acl import when
from ..templates.admin.admintemplate import page as _page
from ..templates.requests import requeststemplate

@when(when.matches(True, 'session.authenticated', True), when.never)
class Admin:
    __dispatch__ = 'resource'
    from .suggestions import Suggestions as suggestions
    from .mistags import Mistags as mistags
    from .auth import Auth as auth
    from .logout import Logout as logout

    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        if len(arg) > 0 and arg[0] != 'requests':
            return "Page not found: {}".format(arg[0])
        requestlist = self.queries.get_new_pending_requests()
        return requeststemplate(_page, "Requests", self._ctx, requestlist)
