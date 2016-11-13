""" Helpers for complex queries, prokyon database """

from ..requestlist import RequestList
from ..played import Played
from ..song import Song
from ..siteoptions import SiteOptions
from sqlalchemy.sql import func, or_
import datetime
from time import time

class Queries:

    def __init__(self, db=None):
        if db is None:
            print("usage: Queries(db='database session')")
        self.db = db
        self.model = None

    @property
    def options(self):
        try:
            return self.__options
        except: # Tried to get options before set, so get the options
            self.options = self.get_options()
            return self.__options

    @options.setter
    def options(self, value):
        self.__options = value

    @property
    def catalogs(self):
        try:
            return self.__catalogs
        except: # Tried to get the catalogs before set, so get the catalogs
            self.catalogs = self.options.catalog.split(",")
            return self.__catalogs

    @catalogs.setter
    def catalogs(self, value):
        self.__catalogs = value

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value): # Allows changing the model used in some queries
        self.__model = value

    def get_total_artists(self):
        return self.db.query(func.count(Song.artist_fullname.distinct()).label('total')).one()

    def get_total_albums(self):
        return self.db.query(func.count(Song.album_fullname.distinct()).label('total')).one()

    def get_top_10(self):
        return self.db.query(func.count(Song.artist_fullname).label('artist_count'),\
                         Song.artist_fullname.label('aid'),\
                         Song.artist_fullname.label('fullname')).\
                         group_by(Song.artist_fullname).\
                         order_by(func.count(Song.artist_fullname).desc()).limit(10)

    def get_total_played_by_me(self):
        return self.db.query(func.count(Played.track_id.distinct()).label('total')).\
                                        join(Song).\
                                        filter(Played.played_by_me == 1).one()

    def get_top_played_by_all(self):
        for tid, tid_count, title, art, alb, date_played in self.db.query(Played.track_id.label('track_id'),\
                         func.count(Played.track_id).label('played_count'),\
                         func.max(Song.title).label('title'),\
                         func.max(Song.artist_fullname).label('artist_fullname'),\
                         func.max(Song.album_fullname).label('album_fullname'),
                         func.max(Played.date_played).label('last_play')).\
                    join(Song).\
                    group_by(Played.track_id).\
                    order_by(func.count(Played.track_id).desc()).limit(10):
            played = self.db.query(Played).filter(Played.track_id==tid, Played.date_played==date_played).one()
            yield played, tid_count, date_played

    def get_top_played_by_me(self):
        return self.get_top_played_by_all()

    def get_top_requested(self):
        for sid, rid, cnt in self.db.query(RequestList.song_id,\
                                       func.max(RequestList.id),\
                                       func.count(RequestList.song_id)).\
                                 join(Song).\
                                 order_by(func.count(RequestList.song_id).desc()).\
                                 group_by(RequestList.song_id).limit(10):
            r = self.db.query(RequestList).join(Song).filter(RequestList.id==rid).one()
            yield r.song

    def get_song_stats(self):
        return self.db.query(func.sum(Song.size).label('song_size'),
                              func.count(Song.id).label('total_songs'),
                              func.avg(Song.size).label('avg_song_size'),
                              func.sum(Song.time).label('song_time'),
                              func.avg(Song.time).label('avg_song_time')).one()

    def get_top_requestors(self):
        return self.db.query(func.count(RequestList.name).label('request_count'),
                         RequestList.name.label('requestor'),
                         func.max(RequestList.t_stamp).label('last_request')).join(Song).group_by(RequestList.name).order_by(func.count(RequestList.name).desc()).limit(10)

    def get_letters_counts(self):
        if self.model == 'Artist':
            return self.db.query(func.upper(func.left(Song.artist_name, 1)).label('letter'), func.count(Song.artist_fullname.distinct()).label('count')).\
                                group_by(func.upper(func.left(Song.artist_name, 1)))
        elif self.model == 'Album':
            return self.db.query(func.upper(func.left(Song.album_name, 1)).label('letter'), func.count(Song.album_fullname.distinct()).label('count')).\
                                group_by(func.upper(func.left(Song.album_name, 1)))

    def get_names_by_letter(self, letter):
        if self.model == 'Album':
            return self.db.query(Song.album_fullname.label('fullname'),\
                         Song.album_fullname.label('aid'),\
                         func.count(Song.title).label('songcount')).\
                         filter(Song.album_name.like(letter+'%')).\
                         order_by(Song.album_name).group_by(Song.album_name)
        elif self.model == 'Artist':
            return self.db.query(Song.artist_fullname.label('fullname'),\
                         Song.artist_fullname.label('aid'),\
                         func.count(Song.title).label('songcount')).\
                         filter(Song.artist_name.like(letter+'%')).\
                         order_by(Song.artist_name).group_by(Song.artist_name)

    def get_artist_album_by_id(self, id):
        if self.model == 'Album':
            f = Song.album_fullname
        elif self.model == 'Artist':
            f = Song.artist_fullname
        a = self.db.query(f.label('fullname'), Song).filter(f == id).first()
        s = self.db.query(Song).filter(f == id)
        return [a.fullname, s]

    def get_song_by_id(self, id):
        return self.db.query(Song).filter(Song.id == id).one()

    def get_new_pending_requests(self):
        return self.db.query(RequestList).\
                                filter((RequestList.status == 'new') | (RequestList.status == 'pending')).order_by(RequestList.id)

    def get_new_pending_requests_info(self):
        return self.db.query(func.count(RequestList.id).label('request_count'),
                  func.sum(Song.time).label('request_length')).\
                  join(Song).filter(or_(RequestList.status=="new", RequestList.status=='pending')).one()

    def get_current_requests(self):
        return self.db.query(RequestList).\
                       filter((RequestList.status == 'new') | (RequestList.status == 'pending')).order_by(RequestList.id)

    def get_all_requests_info(self):
        return self.db.query(func.count(RequestList.status).label('request_count'),
                         RequestList.status,
                         func.sum(Song.time).label('request_length')).\
                         join(Song).group_by(RequestList.status)

    def get_new_counts(self, days=7):
        start_time = time() - 60*60*24*days
        return self.db.query(func.count(Song.id).label('new_count'),\
                         func.sum(Song.time).label('total_time'),\
                         func.sum(Song.size).label('total_size')).\
                         filter(Song.addition_time >= start_time).one()

    def get_new_artists(self, days=7):
        start_time = time() - 60*60*24*days
        for count, total_time, total_size, addition_time, art_name in self.db.query(func.count(Song.artist_fullname).label('artist_count'),
                         func.sum(Song.time).label('artist_time'),
                         func.sum(Song.size).label('artist_size'),
                         func.max(Song.addition_time).label('m_addition_time'),
                         func.max(Song.artist_fullname).label('artist_fullname')
                         ).\
                        filter(Song.addition_time >= start_time).\
                        group_by(func.lower(Song.artist_fullname)).\
                        order_by(func.max(Song.addition_time).desc()):
            song = self.db.query(Song).filter(Song.artist_fullname==art_name,\
                                          Song.addition_time >= start_time).first()
            yield count, total_time, total_size, song

    def get_played_by_me(self):
        return self.db.query(func.count(Played.track_id.distinct()).label('total')).\
                  join(Song).filter(Played.played_by_me == 1).one()

    def get_top_played_by(self, played_by_me=False, limit=10):
        if played_by_me == 'all':
            p = self.db.query(func.count(Played.date_played).label('played_count'),
                              func.max(Played.date_played).label('date_played'), Played).\
                              join(Song).\
                              group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(limit)
        else:
            p = self.db.query(Played, func.count(Played.date_played).label('played_count'),
                            func.max(Played.date_played).label('date_played')).\
                            join(Song).filter(Played.played_by_me == played_by_me).\
                            group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(limit)
        return p

    def get_last_played(self, limit=50):
        return self.db.query(func.count(Played.date_played).label('played_count'), func.avg(Song.time).label('avg_time'), Played).join(Song).\
            group_by(Played.date_played).\
            order_by(Played.date_played.desc()).limit(limit)

    def get_multi_albums(self, artist_name, song_title):
        return self.db.query(Song).filter(func.lower(Song.artist_fullname) == func.lower(artist_name),\
                                      func.lower(Song.title) == func.lower(song_title))

    def full_text_search(self, phrase=None):
        return self.db.query(Song).filter(
                (Song.title.match(phrase) |\
                 Song.artist_fullname.match(phrase) |\
                 Song.album_fullname.match(phrase)))

    def advanced_search(self, search_for=None, phrase=None):
        if search_for == 'title':
            search = Song.title
        elif search_for == 'artist':
            search = Song.artist_name
        elif search_for == 'album':
            search = Song.album_name
        p = r'%'+phrase+r'%'
        r = self.db.query(Song).filter(search.ilike(phrase))
        print("Got results: ", r.count())
        return r
