from .letter import letter
from .letters import letters

from ..templates.tracklist import tracklist

from sqlalchemy.orm.exc import NoResultFound


def get(self, *arg, **args):
	""" Get used for artist and albums. Calling class must define the model via self._db_model """

	if 'id' in args:
		try:
			a = self.queries.get_artist_album_by_id(args['id'])
		except NoResultFound:
			# No error given for now, just go back to the basic letters list
			return letters(self)
		else:
			return tracklist(self._ctx, a) # Need _ctx here, because it's a template
	if 'letter' in args:
		return letter(self, args['letter'])
	else: # All other args are ignored
		return letters(self)

