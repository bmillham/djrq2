""" Just to keep things clean, all queries go here """

#from . import session
from .requestlist import RequestList
from .played import Played
from .song import Song
from .artist import Artist
from .album import Album
from sqlalchemy.sql import func, or_

def get_song_stats(self):
    return self._ctx.db.default.query(func.sum(Song.size).label('song_size'),
                              func.count(Song.id).label('total_songs'),
                              func.avg(Song.size).label('avg_song_size'),
                              func.sum(Song.time).label('song_time'),
                              func.avg(Song.time).label('avg_song_time')).filter(Song.catalog_id.in_(self._ctx._catalogs)).one()

def get_letters_counts(self):
	return self._ctx.db.default.query(func.left(self._db_model.name, 1).label('letter'),
									  func.count(self._db_model.id.distinct()).label('count')).\
									  join(Song).\
									  filter(Song.catalog_id.in_(self._ctx._catalogs)).\
									  group_by(func.left(self._db_model.name, 1))
									  
def get_names_by_letter(self):
	try:
		self._db_model.disk # Fails for artist
	except AttributeError: # Don't use disk in order_by
		names = self._ctx.db.default.query(self._db_model.fullname.label('fullname'),
						self._db_model.id.label('aid'),
						func.count(Song.id).label('songcount')).\
					join(Song).\
					filter(self._db_model.name.startswith(self._ctx.selected_letter), Song.catalog_id.in_(self._ctx._catalogs)).\
					order_by(self._db_model.name).group_by(self._db_model.id)
	else: # Use disk in order_by
		names = self._ctx.db.default.query(self._db_model.fullname.label('fullname'),
						self._db_model.id.label('aid'),
						self._db_model.disk.label('disk'),
						self._db_model.year.label('year'),
						func.count(Song.id).label('songcount')).\
					join(Song).\
					filter(self._db_model.name.startswith(self._ctx.selected_letter), Song.catalog_id.in_(self._ctx._catalogs)).\
					order_by(self._db_model.name, self._db_model.disk, Song.catalog_id.in_(self._ctx._catalogs)).\
					group_by(self._db_model.id)
	return names

def get_artist_album_by_id(self, id):
	return self._ctx.db.default.query(self._db_model).filter(self._db_model.id == id).one()

def get_total_artists(self):
	return self._ctx.db.default.query(func.count(Artist.fullname.distinct()).label('total')).\
										join(Song).filter(Song.catalog_id.in_(self._ctx._catalogs)).one()

def get_total_albums(self):
	return self._ctx.db.default.query(func.count(Album.id.distinct()).label('total')).\
										join(Song).filter(Song.catalog_id.in_(self._ctx._catalogs)).one()

def get_total_played_by_me(self):
	return self._ctx.db.default.query(func.count(Played.track_id.distinct()).label('total')).\
										join(Song).\
										filter(Song.catalog_id.in_(self._ctx._catalogs), Played.played_by_me == 1).one()

def get_top_10(self):
	return self._ctx.db.default.query(func.count(Song.artist_id).label('artist_count'),
						Song.artist_id,
						Artist.fullname.label('artist_fullname')).\
						join(Artist).\
						filter(Song.catalog_id.in_(self._ctx._catalogs)).\
						group_by(Song.artist_id).order_by(func.count(Song.artist_id).desc()).limit(10)

"""





def get_new_pending_requests_info():
    return session.query(func.count(RequestList.id).label('request_count'),
                  func.sum(Song.time).label('request_length')).\
                  join(Song).filter(or_(RequestList.status=="new", RequestList.status=='pending')).one()

def get_all_requests_info():
    return session.query(func.count(RequestList.status).label('request_count'),
                         RequestList.status,
                         func.sum(Song.time).label('request_length')).\
                         join(Song).group_by(RequestList.status)

def get_last_played(catalogs, limit=50):
    return session.query(func.count(Played.date_played), func.avg(Song.time), Played).join(Song).filter(Song.catalog.in_(catalogs)).group_by(Played.date_played).order_by(Played.date_played.desc()).limit(limit)

def get_multi_ablums(artist_name, song_title):
    return session.query(Song).join(Album).join(Artist).filter(Artist.fullname == artist_name, Song.title == song_title)

def get_new_artists(catalogs, start_time):
    return session.query(func.count(Song.artist_id), func.sum(Song.time), func.sum(Song.size), Song).filter(Song.addition_time >= start_time, Song.catalog.in_(catalogs)).order_by(Song.addition_time.desc()).group_by(Song.artist_id)

def get_new_counts(catalogs, start_time):
    return session.query(func.count(Song.id), func.sum(Song.time), func.sum(Song.size)).filter(Song.addition_time >= start_time, Song.catalog.in_(catalogs)).one()



def get_top_played_by_me(catalogs):
    return  session.query(Played,
                          func.count(Played.track_id).label('played_count'),
                          func.max(Played.date_played).label('date_played')).join(Song).filter(Song.catalog.in_(catalogs), Played.played_by_me == 1).group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(10)

def get_top_played_by_all(catalogs):
    return session.query(func.count(Played.track_id), Song, func.max(Played.date_played)).join(Song).filter(Song.catalog.in_(catalogs)).group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(10)
    
def get_top_requested(catalogs):
    return session.query(Song).\
                         join(RequestList).\
                         filter(Song.catalog.in_(catalogs), RequestList.status == 'played').\
                         group_by(RequestList.song_id).\
                         order_by(func.count(RequestList.song_id).desc()).limit(10)

def get_top_requestors(catalogs):
    return session.query(func.count(RequestList.name).label('request_count'),
                         RequestList.name.label('requestor'),
                         func.max(RequestList.t_stamp).label('last_request')).join(Song).filter(Song.catalog.in_(catalogs)).group_by(RequestList.name).order_by(func.count(RequestList.name).desc()).limit(10)

def full_text_search(catalogs, phrase):
    return session.query(Song).join(Artist).join(Album).filter(((Song.title.match(phrase)) | (Artist.name.match(phrase)) | (Album.name.match(phrase))), Song.catalog.in_(catalogs))

def advanced_search(catalogs, search_for, phrase):
    if search_for == 'title':
        search = Song.title
    elif search_for == 'artist':
        search = Artist.name
    elif search_for == 'album':
        search = Album.name
    return session.query(Song).join(Artist).join(Album).filter(search.like(phrase), Song.catalog.in_(catalogs))

def get_current_requests():
    return session.query(RequestList).\
                       filter((RequestList.status == 'new') | (RequestList.status == 'pending')).order_by(RequestList.id)
"""
