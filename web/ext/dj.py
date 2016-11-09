import importlib
from ..app.djrq.model.lastplay import DJs

class DJExtension:
	needs = {'db'}
	
	def __init__(self, whatsnewdays=30):
		self.whatsnewdays = whatsnewdays
	
	def prepare(self, context):
		""" Setup basic stuff needed for all pages """

		context.__dict__['whatsnewdays'] = self.whatsnewdays
		djrow = context.db.lastplay.query(DJs).filter(DJs.dj == context.djname).one()
		context.__dict__['djname'] = djrow.dj

		package = 'web.app.djrq.model.'+djrow.databasetype
		context.__dict__['dbmodel'] = importlib.import_module('.'+djrow.databasetype, 'web.app.djrq.model')
		context.__dict__['queries'] = importlib.import_module('.queries', context.dbmodel.__name__).Queries(db=context.db.default)
		try:
			album = importlib.import_module(package+'.album').Album
		except:
			album = 'Album'
		try:
			artist = importlib.import_module(package+'.artist').Artist
		except:
			artist = 'Artist'
		context.__dict__['artist'] = artist
		context.__dict__['album'] = album
		if context.queries.db is None:
			raise HTTPError("Queries is None!")
		context.__dict__['dbstats'] = context.queries.get_song_stats()
		context.__dict__['requests_info'] = context.queries.get_new_pending_requests_info()
		context.__dict__['new_counts'] = context.queries.get_new_counts(days=context.whatsnewdays)
		try:
			context.__dict__['listeners'] = context.db.default.query(Listeners).one()
		except:
			context.__dict__['listeners'] = None
		context.__dict__['alldjs'] = context.db.lastplay.query(DJs).filter(DJs.hide_from_menu == 0).order_by(DJs.dj)

