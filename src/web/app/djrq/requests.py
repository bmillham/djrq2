# encoding: utf-8

import importlib
from .templates.requests import requeststemplate
from .templates.requestwindow import requestwindowtemplate1
from datetime import datetime

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

		requestlist = self.queries.get_new_pending_requests()
		return requeststemplate("Current Requests", self._ctx, requestlist)

	def post(self, *arg, **args):
		if args['formtype'] == 'request':
			RequestList = importlib.import_module('.requestlist', self._ctx.DbModel.__name__).RequestList
			now = datetime.utcnow()
			new_row = RequestList(song_id=args['tid'],
								  t_stamp=now,
								  host=self._ctx.response.request.remote_addr,
								  msg=args['comment'],
								  name=args['sitenick'],
								  code=0,
								  eta=now,
								  status='new')
			self._ctx.db.add(new_row)
			self._ctx.db.commit()
			newcount = self._ctx.queries.get_new_pending_requests_info().request_count
			return {'html': 'Thank you for your request {}'.format(args['sitenick']),
				'tid': args['tid'],
				'newcount': newcount}

		print('Got a mistag post', arg, args)
		return {'html': 'Mistag Accepted: {} {}'.format(args['tid'], args['sitenick']),
				'tid': args['tid']}
