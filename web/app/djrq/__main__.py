# encoding: utf-8

__import__('cinje')

from web.core import Application
from web.ext.annotation import AnnotationExtension
from web.ext.debug import DebugExtension
from web.ext.serialize import SerializationExtension
from web.ext.db import DatabaseExtension
from web.db.sa import SQLAlchemyConnection
from web.ext.selective import SelectiveDefaultDatabase
from web.ext.dj import DJExtension
from web.ext.djhost import DJHostExtension

# Import the lastplay model now, to get DJ database information
from web.app.djrq.model.lastplay import DJs

from .root import Root
from .dbconfig import lastplay_url

class FakeContext:
	""" A fake session, just used to query the database """
	def __init__(self):
		self.db = {}

# Get the list of DJs and databases from the lastplay database
# and setup the SQLAlchemy connections
#lastplay_url = 'mysql://gothalice:GARules@dbserver.millham.net/lastplay'
databases = {'lastplay': SQLAlchemyConnection(lastplay_url)}
context = FakeContext()
databases['lastplay'].start(context)
djs = databases['lastplay'].Session.query(DJs).filter(DJs.hide_from_menu == 0)
for d in djs:
	server = "themaster.millham.net" if d.server == "localhost" else d.server
	url = "mysql://{}:{}@{}/{}?charset=utf8".format(d.user, d.password, server, d.db)
	databases[d.dj.lower()] = SQLAlchemyConnection(url)
	print(d.user, d.password, server)

databases['lastplay'].stop(context)

app=Application(Root, extensions=[
		AnnotationExtension(),
		DebugExtension(),
		SerializationExtension(),
		DatabaseExtension(
			**databases
			),
		SelectiveDefaultDatabase(),
		DJExtension(),
		DJHostExtension(),
		])



if __name__ == "__main__":
	app.serve('wsgiref', host='0.0.0.0')
