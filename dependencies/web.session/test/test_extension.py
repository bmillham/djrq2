# encoding: utf-8

from __future__ import unicode_literals

from datetime import timedelta
from webob import Request
from webob.cookies import Cookie

from web.core import Application
from web.ext.serialize import SerializationExtension
from web.ext.session import SessionExtension


class TestSessionExtension(object):
	def test_construction_defaults(self):
		se = SessionExtension()
		assert se.refreshes
		assert se.cookie == {'name': 'session', 'httponly': True, 'path': '/'}
		assert 'default' in se.engines
		assert se.engines['default'].__class__.__name__ == 'MemorySession'
	
	def test_construction_expires(self):
		se = SessionExtension(expires=24)
		assert se.expires == 24 * 60 * 60
		
		se = SessionExtension(expires=timedelta(days=2))
		assert se.expires == 2 * 24 * 60 * 60


class TestSessionUsage(object):
	class Root(object):
		def __init__(self, context):
			self._ctx = context
		
		def nop(self):
			return "nop"
		
		def id(self):
			return str(self._ctx.session._id)
		
		def get(self):
			data = dict(self._ctx.session.default)
			data['_id'] = str(self._ctx.session._id)
			return data
		
		def set(self, **kw):
			self._ctx.session.default.update(kw)
			return "updated"
	
	@classmethod 
	def setup_class(cls):
		"""Construct the application to test against."""
		
		ext = SessionExtension()
		cls.sessions = ext.engines['default']._sessions
		
		cls.app = Application(cls.Root, extensions=[
				SerializationExtension(),
				ext,
			])
		
		cls.cookies = {}
	
	def _update_cookies(self, response):
		cookies = Cookie()
		
		# Load any generated cookies.
		for cookie in response.headers.getall('Set-Cookie'):
			cookies.load(cookie)
		
		self.cookies.update({i.name.decode('ascii'): i.value.decode('ascii') for i in cookies.values()})
	
	def get(self, path):
		req = Request.blank(path, cookies=self.cookies)
		resp = req.get_response(self.app)
		assert resp.status_int == 200
		self._update_cookies(resp)
		return resp
	
	def post(self, path, **data):
		req = Request.blank(path, cookies=self.cookies, method='POST')
		req.content_type = "application/json"
		req.json = data
		resp = req.get_response(self.app)
		assert resp.status_int == 200
		self._update_cookies(resp)
		return resp
	
	def test_session(self):
		response = self.get('/nop')  # Do not touch a session.
		assert not self.sessions
		
		# This should create a session, and set a cookie.
		response = self.get('/get')  # Request the contents of the session.
		assert self.sessions
		
		contents = response.json
		sid = contents.get('_id', None)
		assert sid in self.sessions
		
		response = self.get('/id')  # Request the session ID.
		assert len(sid) == 24
		assert sid == response.text.strip()
		
		response = self.post('/set', name="Alice", age=27)
		assert response.text == "updated"
		
		response = self.get('/get')  # Request the contents of the session.
		
		contents = response.json
		assert contents == {'_id': sid, 'name': "Alice", 'age': 27}

