# encoding: utf-8

class Album:
	__dispatch__ = 'resource'
	__resource__ = 'album'

	from .common.get import get

	def __init__(self, context, name, *arg, **args):
		self._ctx = context
		self.queries = context.queries
		self.queries.model = context.Album # Pass the DB model to get
