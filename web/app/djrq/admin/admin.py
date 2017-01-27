# encoding: utf-8

from web.ext.acl import when
from ..templates.admin.admintemplate import page as _page
from ..templates.admin.requests import requeststemplate, requestrow
from ..templates.requests import requestrow as rr
from ..send_update import send_update
import cinje

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
    from .changepw import ChangePassword as changepw
    from .showhistory import ShowHistory as showhistory
    from .restoredatabase import RestoreDatabase as restoredatabase

    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        if len(arg) > 0 and arg[0] != 'requests':
            return "Page not found: {}".format(arg[0])
        if 'view_status' not in args:
            args['view_status'] = 'New/Pending'
        if 'change_status' in args:
            changed_row = self.queries.change_request_status(args['id'], args['status'])

            try:
                request_row = cinje.flatten(rr(changed_row))
            except:
                request_row = '' # Row was deleted

            np_info = self.queries.get_requests_info(status=args['view_status'])
            send_update(self._ctx.websocket, requestbutton=np_info.request_count, request_row=request_row, new_request_status=args['status'], request_id=args['id']) # Update the request count button
            send_update(self._ctx.websocket_admin, requestbutton=np_info.request_count) # Update the request count button

        requestlist = self.queries.get_requests(status=args['view_status'])

        try:
            requestinfo = np_info
        except:
            requestinfo = self.queries.get_requests_info(status=args['view_status'])

        return requeststemplate(_page, "Requests", self._ctx, requestlist=requestlist, view_status=args['view_status'], requestinfo=requestinfo)
