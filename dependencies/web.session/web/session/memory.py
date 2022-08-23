# encoding: utf-8

"""Session handling extension using session engines."""

from threading import Lock, Timer
from datetime import datetime, timedelta

from web.core.context import Context


log = __import__('logging').getLogger(__name__)



class PeriodicExpiration(object):
	"""Periodically clean up stale sessions."""
	
	def __init__(self, pool, period=60):
		self.pool = pool
		self._stop = False
		self.period = period
		self.timer = None
		self.lock = Lock()
	
	def start(self):
		self.schedule()
	
	def _run(self):
		with self.lock:
			self.timer = None
		
		cull = set()  # The set of session IDs to remove.
		now = datetime.utcnow()
		
		for sid in self.pool:
			if '_expires' not in self.pool[sid]: continue
			if self.pool[sid]['_expires'] <= now:
				cull.add(sid)
		
		for sid in cull:  # Can't remove while iterating above...
			del self.pool[sid]
		
		self.schedule()
	
	def schedule(self):
		if self._stop:
			return
		
		with self.lock:
			self.timer = Timer(self.period, self._run)
			self.timer.name = "memory-session-expunge"
		
		self.timer.start()
	
	def stop(self):
		self._stop = True
		
		if self.timer:
			self.timer.stop()


class MemorySession(object):
	def __init__(self, expire=None, refresh=True):
		"""Initialize in-memory session storage."""
		
		self._sessions = {}
		
		if expire and hasattr(expire, 'isdigit') and expire.isdigit():
			expire = timedelta(hours=expire)
		
		self._expire = expire
		self._refresh = refresh
		
		if expire:
			self._expunge = PeriodicExpiration()
	
	def start(self, context):
		"""Spawn the auto-expunge thread on startup if configured to do so."""
		if self._expire: self._expunge.start()
	
	def stop(self, context):
		"""Shut down the auto-expunge thread if one was configured."""
		if self._expire: self._expunge.stop()
	
	def is_valid(self, context, sid):
		"""Identify if the given session ID is valid in our stores."""
		return sid in self._sessions
	
	def invalidate(self, context, sid):
		"""Delete our storage of the given session."""
		return self._sessions.pop(sid, None) is not None
	
	def __get__(self, session, type=None):
		"""Retrieve the current session, or create one within our stores if missing."""
		
		if session is None:
			return self
		
		now = datetime.utcnow()
		sid = str(session._id)
		
		if sid not in self._sessions:
			if __debug__:
				log.debug("Constructing new in-memory session.")
			
			self._sessions[sid] = Context()
		
		elif self._expire and '_expires' in self._sessions[sid] and self._sessions[sid]._expires <= now:
			if __debug__:
				log.debug("Recreating expired in-memory session.")
			
			self._sessions[sid] = Context()
		
		elif __debug__:
			log.debug("Loading existing in-memory session.")
		
		session[self.name] = self._sessions[sid]
		
		return self._sessions[sid]
	
	def persist(self, context):
		"""Perform the work of saving modified session data back out.
		
		The in-memory representation is modified "live" in-place, so this only updates our expiry time.
		"""
		if __debug__:
			log.debug("Persisting in-memory session.")
		
		if self._expire and (self._refresh or '_expires' not in getattr(context.session, self.name)):
			getattr(context.session, self.name)._expires = datetime.utcnow() + self._expire

