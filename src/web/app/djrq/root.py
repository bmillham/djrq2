# encoding: utf-8

import importlib
from webob.exc import HTTPFound, HTTPError, HTTPNotFound
from web.app.static import static
from .templates.notfound import notfound
from .templates.tracklist import tracklist
from .model.lastplay import DJs
from .model.common import Listeners
import os

class Root:
	__dispatch__ = 'resource'

	# Import the album, artist, stats, requests and lastplayed endpoints.
	from .album import Album as album, Album
	from .artist import Artist as artist, Artist
	from .stats import Stats as stats, Stats
	from .requests import Requests as requests, Requests
	from .lastplayed import LastPlayed as lastplayed
	from .whatsnew import WhatsNew as whatsnew


	public = static(os.path.join(os.path.dirname(__file__), 'public'))

	def __init__(self, context=None, collection=None, record=None):
		""" Setup basic stuff needed for all pages """
		self._ctx = context
		# Get listeners
		try:
			self._ctx.listeners = context.db.default.query(Listeners).one()
		except:
			self._ctx.listeners = None

		# Get list of all DJs
		self._ctx.alldjs = context.db.lastplay.query(DJs).filter(DJs.hide_from_menu == 0).order_by(DJs.dj)

		# Import the proper models, based on the database type
		host, sep, dom = context.request.host.partition(".")
		if '-' in host:
			prefix, host = host.split('-') # Strip leading dj-
		else:
			prefix = ''
		djrow = context.db.lastplay.query(DJs).filter(DJs.dj == host).one()
		self._ctx.DjName = djrow.dj
		self._ctx.ServerName = dom
		self._ctx.DjPrefix = prefix
		self._ctx.WhatsNewDays = 30
		package = 'web.app.djrq.model.'+djrow.databasetype
		Queries = importlib.import_module(package+'.queries').Queries
		try:
			self._ctx.Album = importlib.import_module(package+'.album').Album
		except:
			self._ctx.Album = 'Album'
		try:
			self._ctx.Artist = importlib.import_module(package+'.artist').Artist
		except:
			self._ctx.Artist = 'Artist'
		self._ctx.queries = Queries(db=self._ctx.db.default)
		if self._ctx.queries.db is None:
			raise HTTPError("Queries is None!")
		self._ctx.dbstats = self._ctx.queries.get_song_stats()
		self._ctx.requests_info = self._ctx.queries.get_new_pending_requests_info()
		self._ctx.new_counts = self._ctx.queries.get_new_counts(days=self._ctx.WhatsNewDays)

	def get(self, *arg, **args):
		""" Handle other endpoints not imported """
		if len(arg) == 0:
			return HTTPFound(location="/lastplayed") # Make lastplayed the default
		else:
			return notfound(self._ctx, arg[0])

	def post(self, content, *arg, **args):
		print("Got a post", content, arg, args )
		if content == 'search':
			if 'stext' not in args:
				l = self._ctx.queries.advanced_search(search_for=args['advsearchtype'].lower(), phrase=args['advsearchtext'])
				tl = tracklist(self._ctx, l, dataonly=True, phrase='{advsearchtype}: {advsearchtext}'.format(**args))
				r = ""
				for i in tl:
					r += i
				return {'html' : r}
				#return tracklist(self._ctx, l)
				#return {'html': 'Search for {advsearchtype} {advsearchtext}'.format(**args)}
			else:
				l = self._ctx.queries.full_text_search(phrase=args['stext'])
				return tracklist(self._ctx, l, phrase=args['stext'])
		return notfound(self._ctx, content)
