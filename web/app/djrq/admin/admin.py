# encoding: utf-8

from web.ext.acl import when
from ..templates.admin.admintemplate import page as _page
from ..templates.admin.requests import requeststemplate

@when(when.matches(True, 'session.authenticated', True), when.never)
class Admin:
    __dispatch__ = 'resource'
    __resource__ = 'admin'

    from .suggestions import Suggestions as suggestions
    from .mistags import Mistags as mistags
    from .auth import Auth as auth
    from .logout import Logout as logout
    from .showinfo import ShowInfo as showinfo
    from .requestoptions import RequestOptions as requestoptions
    from .catalogoptions import CatalogOptions as catalogoptions
    from .uploadfiles import UploadFiles as uploadfiles
    from .updatedatabase import UpdateDatabase as updatedatabase

    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        if len(arg) > 0 and arg[0] != 'requests':
            return "Page not found: {}".format(arg[0])
        if 'change_status' in args:
            self.queries.change_request_status(args['id'], args['status'])
        requestlist = self.queries.get_new_pending_requests()
        return requeststemplate(_page, "Requests", self._ctx, requestlist)
