from web.ext.db import DatabaseExtension
from web.db.sa import SQLAlchemyConnection
from ..app.djrq.dbconfig import lastplay_url
from web.app.djrq.model.lastplay import DJs


class FakeContext:
	""" A fake session, just used to query the database """
	def __init__(self):
		self.db = {}

class DJDatabaseExtension(DatabaseExtension):
	_needs = {'djhost'}
	_provides = {'djdb', 'db'}

	def __init__(self, default=None, session=None):
		self.needs = set(self._needs)
		self.provides = set(self._provides)

		engines = {'lastplay': SQLAlchemyConnection(lastplay_url)}
		context = FakeContext()
		engines['lastplay'].start(context)
		djs = engines['lastplay'].Session.query(DJs).filter(DJs.hide_from_menu == 0)

		for d in djs:
			# TODO: make this configurable
			server = "themaster.millham.net" if d.server == "localhost" else d.server
			url = "mysql://{}:{}@{}/{}?charset=utf8".format(d.user, d.password, server, d.db)
			engines[d.dj.lower()] = SQLAlchemyConnection(url)
			print(d.user, d.password, server)

		engines['lastplay'].stop(context)
		#if default:
		#	engines['default'] = default
		super(DJDatabaseExtension, self).__init__(default, **engines)
