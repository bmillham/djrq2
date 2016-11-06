# encoding: utf-8

from .templates.requests import requeststemplate
from .templates.requestwindow import requestwindowtemplate1

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
		print('Got a request post', arg, args)
		return {'html': 'Request Accepted: {} {}'.format(args['tid'], args['sitenick']),
				'tid': args['tid']}
