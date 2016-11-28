from ..requestlist import RequestList
from ..played import Played
from ..song import Song
from ..artist import Artist
from ..album import Album
from ..siteoptions import SiteOptions
from ..users import Users
from ..suggestions import Suggestions
from ..mistags import Mistags
from ..catalog import Catalog
from sqlalchemy.sql import func, or_
from sqlalchemy.orm.exc import NoResultFound


from time import time
import hashlib # Used to verify admin passwords
#import scrypt # Add this

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

    def verify_user(self, uname, pword):
        try:
            self.db.query(Users).\
                    filter(Users.uname == uname,
                    Users.pword == hashlib.md5(pword.encode()).hexdigest()).one()
            return True
        except NoResultFound:
            return False

    def get_options(self):
        return self.db.query(SiteOptions).one()

    def get_song_stats(self):
        return self.db.query(func.sum(Song.size).label('song_size'),
                                        func.count(Song.id).label('total_songs'),
                                        func.avg(Song.size).label('avg_song_size'),
                                        func.sum(Song.time).label('song_time'),
                                        func.avg(Song.time).label('avg_song_time')).\
                                        filter(Song.catalog_id.in_(self.catalogs)).one()

    def get_total_artists(self):
        return self.db.query(func.count(Artist.fullname.distinct()).label('total')).\
                                        join(Song).filter(Song.catalog_id.in_(self.catalogs)).one()

    def get_total_albums(self):
        return self.db.query(func.count(Album.id.distinct()).label('total')).\
                                        join(Song).filter(Song.catalog_id.in_(self.catalogs)).one()

    def get_total_played_by_me(self):
        return self.db.query(func.count(Played.track_id.distinct()).label('total')).\
                                        join(Song).\
                                        filter(Song.catalog_id.in_(self.catalogs), Played.played_by_me == 1).one()

    def get_top_10(self):
        return self.db.query(func.count(Song.artist_id).label('artist_count'),
                        Song.artist_id.label('aid'),
                        Artist.fullname.label('fullname')).\
                        join(Artist).\
                        filter(Song.catalog_id.in_(self.catalogs)).\
                        group_by(Song.artist_id).order_by(func.count(Song.artist_id).desc()).limit(10)

    def get_letters_counts(self):
        return self.db.query(func.left(self.model.name, 1).label('letter'),
                                      func.count(self.model.id.distinct()).label('count')).\
                                      join(Song).\
                                      filter(Song.catalog_id.in_(self.catalogs)).\
                                      group_by(func.left(self.model.name, 1))

    def get_names_by_letter(self, letter):
        try:
            self.model.disk # Fails for artist
        except AttributeError: # Don't use disk in order_by
            names = self.db.query(self.model.fullname.label('fullname'),
                        self.model.id.label('aid'),
                        func.count(Song.id).label('songcount')).\
                        join(Song).\
                        filter(self.model.name.startswith(letter), Song.catalog_id.in_(self.catalogs)).\
                        order_by(self.model.name).group_by(self.model.id)
        else: # Use disk in order_by
            names = self.db.query(self.model.fullname.label('fullname'),
                            self.model.id.label('aid'),
                            self.model.disk.label('disk'),
                            self.model.year.label('year'),
                            func.count(Song.id).label('songcount')).\
                        join(Song).\
                        filter(self.model.name.startswith(letter), Song.catalog_id.in_(self.catalogs)).\
                        order_by(self.model.name, self.model.disk).\
                        group_by(self.model.id)
        return names

    def get_artist_album_by_id(self, id):
        return self.db.query(self.model).filter(self.model.id == id).one()

    def get_song_by_id(self, id):
        return self.db.query(Song).filter(Song.id == id).one()

    def get_last_played(self, count=50):
        return self.db.query(func.count(Played.date_played).label('played_count'),\
                                            func.avg(Song.time).label('avg_time'),\
                                            Played).join(Song).\
                                            filter(Song.catalog_id.in_(self.catalogs)).\
                                            group_by(Played.date_played).\
                                            order_by(Played.date_played.desc()).limit(count)

    def get_new_pending_requests(self):
        return self.db.query(RequestList).\
                    filter((RequestList.status == 'new') | (RequestList.status == 'pending')).order_by(RequestList.id)

    def get_new_pending_requests_info(self):
        return self.db.query(func.count(RequestList.id).label('request_count'),
                  func.sum(Song.time).label('request_length')).\
                  join(Song).filter(or_(RequestList.status=="new", RequestList.status=='pending')).one()

    def get_all_requests_info(self):
        return self.db.query(func.count(RequestList.status).label('request_count'),
                         RequestList.status,
                         func.sum(Song.time).label('request_length')).\
                         join(Song).group_by(RequestList.status)

    def get_multi_albums(self, artist_name, song_title):
        #ctx.db.default.query(Song).join(Album).join(Artist).filter(Artist.fullname == r.Played.song.artist.fullname, Song.title == r.Played.song.title)
        return self.db.query(Song).join(Album).join(Artist).filter(Artist.fullname == artist_name, Song.title == song_title)

    def get_new_artists(self, days=7):
        start_time = time() - 60*60*24*days

        return self.db.query(func.count(Song.artist_id).label('new_count'), func.sum(Song.time), func.sum(Song.size), Song).\
                            filter(Song.addition_time >= start_time, Song.catalog_id.in_(self.catalogs)).\
                            order_by(Song.addition_time.desc()).group_by(Song.artist_id)


    def get_new_counts(self, days=180):
        start_time = time() - 60*60*24*days

        return self.db.query(func.count(Song.id).label('new_count'), func.sum(Song.time), func.sum(Song.size)).\
                            filter(Song.addition_time >= start_time, Song.catalog_id.in_(self.catalogs)).one()

    def get_top_played_by(self, played_by_me=False, limit=10):
        if played_by_me == 'all':
            p = self.db.query(func.count(Played.date_played).label('played_count'),
                            func.max(Played.date_played).label('date_played'), Played).\
                            join(Song).filter(Song.catalog_id.in_(self.catalogs)).\
                            group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(limit)
        else:
            p = self.db.query(Played, func.count(Played.date_played).label('played_count'),
                            func.max(Played.date_played).label('date_played')).\
                            join(Song).filter(Song.catalog_id.in_(self.catalogs), Played.played_by_me == played_by_me).\
                            group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(limit)
        return p

    def get_top_requested(self, limit=10):
        return self.db.query(Song).join(RequestList).\
                        filter(Song.catalog_id.in_(self.catalogs), RequestList.status == 'played').\
                        group_by(RequestList.song_id).\
                        order_by(func.count(RequestList.song_id).desc()).limit(limit)

    def get_top_requestors(self, limit=10):
        return self.db.query(func.count(RequestList.name).label('request_count'),
                            RequestList.name.label('requestor'),
                            func.max(RequestList.t_stamp).label('last_request')).\
                            join(Song).filter(Song.catalog_id.in_(self.catalogs)).group_by(RequestList.name).\
                            order_by(func.count(RequestList.name).desc()).limit(limit)

    def full_text_search(self, phrase):
        return self.db.query(Song).join(Artist).join(Album).\
                filter(((Song.title.match(phrase)) | (Artist.name.match(phrase)) | (Album.name.match(phrase))), Song.catalog_id.in_(self.catalogs))

    def advanced_search(self, search_for, phrase):
        search = {'title': Song.title,
             'artist': Artist.name,
             'album': Album.name}
        return self.db.query(Song).join(Artist).join(Album).filter(search[search_for].like(phrase), Song.catalog_id.in_(self.catalogs))

    def get_current_requests(self):
        return self.db.query(RequestList).\
                        filter((RequestList.status == 'new') | (RequestList.status == 'pending')).order_by(RequestList.id)

    def get_suggestions(self):
        return self.db.query(Suggestions)

    def delete_suggestion(self, id):
        row = self.db.query(Suggestions).filter(Suggestions.id==id).one()
        self.db.delete(row)
        return self.db.commit()

    def get_mistags(self):
        return self.db.query(Mistags)

    def delete_mistag(self, id):
        row = self.db.query(Mistags).filter(Mistags.id==id).one()
        self.db.delete(row)
        return self.db.commit()

    def change_request_status(self, id, status):
        row = self.db.query(RequestList).filter(RequestList.id==id).one()
        if status == 'delete':
            self.db.delete(row)
        else:
            row.status = status
        return self.db.commit()

    def get_siteoptions(self):
        return self.db.query(SiteOptions).one()

    def save_siteoptions(self, **args):
        row = self.db.query(SiteOptions).filter(SiteOptions.id==args['sid']).one()
        for field in args:
            if field == 'cat_group':
                row.catalog = ','.join(args[field])
            elif field != 'sid':
                row.__setattr__(field, args[field])
        return self.db.commit()

    def get_catalogs(self):
        return self.db.query(Catalog).order_by(Catalog.name)
