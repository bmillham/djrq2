# encoding: utf-8

from .templates.template import page as _page
from .templates.requests import requeststemplate, requestrow
from .templates.admin.requests import requestrow as adminrequestrow
from .templates.requestwindow import requestwindowtemplate1
from datetime import datetime
from .send_update import send_update
import cinje

class Requests:
    __dispatch__ = 'resource'
    __resource__ = 'requests'


    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        if 'id' in args:
            s = self.queries.get_song_by_id(id=args['id'])
            return requestwindowtemplate1('New Request', self._ctx, s)

        requestlist = self.queries.get_requests()
        return requeststemplate(_page, "Current Requests", self._ctx, requestlist)

    def post(self, *arg, **args):
        now = datetime.utcnow()
        if not self._ctx.session.sitenick:
            self._ctx.session.sitenick = args['sitenick']
        sn = self._ctx.session.sitenick
        if args['formtype'] == 'request':
            new_row = self._ctx.requestlist(song_id=args['tid'],
                                  t_stamp=now,
                                  host=self._ctx.response.request.remote_addr,
                                  msg=args['comment'],
                                  name=sn,
                                  code=0,
                                  eta=now,
                                  status='new')
            self._ctx.db.add(new_row)
            self._ctx.db.commit()
            newcount = self._ctx.queries.get_requests_info().request_count
            request_row = cinje.flatten(requestrow(new_row))
            admin_request_row = cinje.flatten(adminrequestrow(new_row))
            send_update(self._ctx.websocket, requestbutton=newcount, request_row=request_row, request_id=args['tid']) # Update the request count button
            send_update(self._ctx.websocket_admin, requestbutton=newcount, request_row=admin_request_row) # Update the request count button
            return {'html': 'Thank you for your request {}'.format(sn),
                'tid': args['tid'],
                'sitenick': sn,
                'newcount': newcount}
        elif args['formtype'] == 'mistag':
            new_row = self._ctx.mistags(track_id=args['tid'],
                              reported=now,
                              reported_by=sn,
                              comments=args['comment'],
                              title=args['title'],
                              artist=args['artist'],
                              album=args['album'])
            self._ctx.db.add(new_row)
            self._ctx.db.commit()
            return {'html': 'Thank you for your Mistag report {}'.format(sn),
                'sitenick': sn,
                'tid': args['tid']}
        elif args['formtype'] == 'suggestion':
            new_row = self._ctx.suggestions(
                                            comments="{} {}".format(args['comment'], now),
                                            title=args['title'],
                                            artist=args['artist'],
                                            album=args['album'],
                                            suggestor=sn,
                                            )
            self._ctx.db.add(new_row)
            self._ctx.db.commit()
            return {'html': "Thank you for your suggestion",
                    'sitenick': sn,}
