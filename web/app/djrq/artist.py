class Artist:
	__dispatch__ = 'resource'
	__resource__ = 'artist'

	from .common.get import get

	def __init__(self, context, name, *arg, **args):
		self._ctx = context
		self.queries = context.queries
		self.queries.model = context.Artist


