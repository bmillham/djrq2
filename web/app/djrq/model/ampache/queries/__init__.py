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
import sqlalchemy
from sqlalchemy.sql import func, or_, and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.serializer import dumps # For backing up tables.


from time import time
from datetime import datetime

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

    def get_metadata_fields(self):
        return self.db.query(SiteOptions.metadata_fields).limit(1).one()

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

    def get_top_10(self, limit=10):
        return self.db.query(func.count(Song.artist_id).label('artist_count'),
                        Song.artist_id.label('aid'),
                        Artist.fullname.label('fullname')).\
                        join(Artist).\
                        filter(Song.catalog_id.in_(self.catalogs)).\
                        group_by(Song.artist_id).order_by(func.count(Song.artist_id).desc()).limit(limit)

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

    def get_artist(self, artist):
        return self.db.query(Artist).filter(Artist.fullname == artist)

    def get_album(self, artist_id, album):
        return self.db.query(Song).join(Artist).join(Album).\
            filter((Artist.id == artist_id) & (Album.prename == album))

    def get_title(self, artist_id, title):
        return self.db.query(Song).\
            filter((Song.artist_id == artist_id) & (Song.title == title))

    def get_artist_album_by_id(self, id, days=None):
        if days is not None:
            start_time = time() - 60*60*24*days
            return self.db.query(Song).join(self.model).filter(self.model.id == id, Song.addition_time >= start_time).order_by(Song.title)
        else:
            return self.db.query(self.model).filter(self.model.id == id).one()

    def get_song_by_id(self, id):
        return self.db.query(Song).filter(Song.id == id).one()

    def get_song_by_art_title_alb(self, art=None, title=None, alb=None):
        return self.db.query(Song).filter(Song.artist.name == art)

    def get_last_played(self, count=50):
        try:
            return self.db.query(func.count(Played.date_played).label('played_count'),\
                                            func.avg(Song.time).label('avg_time'),\
                                            Played).join(Song).\
                                            filter(Song.catalog_id.in_(self.catalogs)).\
                                            group_by(Played.date_played).\
                                            order_by(Played.date_played.desc()).limit(count)
                                            #order_by(Played.played_id).limit(count)
        except sqlalchemy.exc.OperationalError:
            return self.db.query(func.count(Played.date_played).label('played_count'), \
                                 func.avg(Song.time).label('avg_time'), \
                                 Played).join(Song). \
                filter(Song.catalog_id.in_(self.catalogs)). \
                group_by(Played.date_played). \
                group_by(Played.played_id). \
                order_by(Played.date_played.desc()).limit(count)


    def get_requests(self, status='New/Pending', id=None):
        if id:
            return self.db.query(RequestList).filter(or_(*[RequestList.status == s for s in status.split('/')]),
                                                     and_(RequestList.song_id == id)).order_by(RequestList.id)
        else:
            return self.db.query(RequestList).filter(or_(*[RequestList.status == s for s in status.split('/')])).order_by(RequestList.id)

    def update_request_to_played(self, request_id):
        self.db.query(RequestList).filter(RequestList.id == request_id).update({'status': 'played'})
        self.db.commit()

    def get_requests_info(self, status='New/Pending'):
        return self.db.query(func.count(RequestList.id).label('request_count'),
                  func.sum(Song.time).label('request_length')).\
                  join(Song).filter(or_(*[RequestList.status == s for s in status.split('/')])).one()

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

        try:
            return self.db.query(func.count(Song.artist_id).label('new_count'), func.sum(Song.time), func.sum(Song.size), Song).\
                            filter(Song.addition_time >= start_time, Song.catalog_id.in_(self.catalogs)).\
                            order_by(Song.addition_time.desc()).group_by(Song.artist_id)
        except sqlalchemy.exc.OperationalError:
            return self.db.query(func.count(Song.artist_id).label('new_count'), func.sum(Song.time),
                                 func.sum(Song.size), Song). \
                filter(Song.addition_time >= start_time, Song.catalog_id.in_(self.catalogs)).\
                order_by(Song.addition_time.desc()).group_by(Song.artist_id).group_by(Song.catalog)


    def get_new_counts(self, days=180):
        start_time = time() - 60*60*24*days

        return self.db.query(func.count(Song.id).label('new_count'), func.sum(Song.time), func.sum(Song.size)).\
                            filter(Song.addition_time >= start_time, Song.catalog_id.in_(self.catalogs)).one()

    def get_top_played_by(self, played_by_me=False, limit=10):
        if played_by_me == 'all':
            p = self.db.query(func.count(Played.date_played).label('played_count'),
                            func.max(Played.date_played).label('date_played'), Played).\
                            join(Song).join(Artist).filter(Song.catalog_id.in_(self.catalogs)).\
                            group_by(Song.title, Artist.fullname).order_by(func.count(Played.track_id).desc()).limit(limit)
        else:
            p = self.db.query(Played, func.count(Played.date_played).label('played_count'),
                            func.max(Played.date_played).label('date_played')).\
                            join(Song).join(Artist).filter(Song.catalog_id.in_(self.catalogs), Played.played_by_me == played_by_me).\
                            group_by(Song.title, Artist.fullname).order_by(func.count(Played.track_id).desc()).limit(limit)
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

    def get_song_by_ata(self, artist, title, album):
        if type(album) is not list:
            album = [album]
        if type(title) is not list:
            title = [title]
        return self.db.query(Song).join(Artist).join(Album).\
            filter(Song.catalog_id.in_(self.catalogs)).\
            filter(Album.prename.in_(album)).\
            filter(Artist.fullname == artist).\
            filter(Song.title.in_(title))

    def get_song_by_artist_title(self, artist, title):
        return self.db.query(Song).join(Artist).join(Album).\
            filter(Song.catalog_id.in_(self.catalogs)).\
            filter(Artist.fullname == artist).\
            filter(Song.title == title)

    def add_played_song(self, track_id, played_by, played_by_me):
        np = Played(track_id=track_id, date_played=datetime.utcnow(), played_by=played_by, played_by_me=played_by_me)
        self.db.add(np)
        self.db.commit()

    def get_artist_with_dash(self):
        return self.db.query(Artist).filter(Artist.name.match(' - '))

    def get_album_with_dash(self, artist):
        return self.db.query(Song).join(Artist).join(Album).\
            filter(((Artist.name == artist) & (Album.name.match(' ' ))))
        
    def full_text_search(self, phrase):
        return self.db.query(Song).join(Artist).join(Album).\
                filter(((Song.title.match(phrase)) | (Artist.name.match(phrase)) | (Album.name.match(phrase))), Song.catalog_id.in_(self.catalogs)).order_by(Song.title)

    def advanced_search(self, search_for, phrase):
        search = {'title': Song.title,
             'artist': Artist.name,
             'album': Album.name}
        return self.db.query(Song).join(Artist).join(Album).filter(search[search_for].like(phrase), Song.catalog_id.in_(self.catalogs)).order_by(search[search_for])

    def get_current_requests(self):
        return self.db.query(RequestList).\
                        filter((RequestList.status == 'new') | (RequestList.status == 'pending')).order_by(RequestList.id)

    def get_suggestions(self):
        return self.db.query(Suggestions)

    def delete_suggestion(self, id):
        row = self.db.query(Suggestions).filter(Suggestions.id==id).one()
        self.db.delete(row)
        return self.db.commit()

    def get_suggestions_count(self):
        return self.db.query(func.count(Suggestions.id).label('suggestions_count')).one()

    def get_mistags_count(self):
        return self.db.query(func.count(Mistags.id).label('mistags_count')).one()

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
        self.db.commit()
        return row

    def get_siteoptions(self):
        return self.db.query(SiteOptions).one()

    def save_siteoptions(self, **args):
        row = self.db.query(SiteOptions).filter(SiteOptions.id==args['sid']).one()
        for field in args:
            if field == 'cat_group':
                row.catalog = ','.join(args[field])
            elif field == 'strict_metadata':
                row.strict_metadata = int(args[field])
            elif field == 'auto_update_requests':
                row.auto_update_requests = int(args[field])
            elif field != 'sid':
                row.__setattr__(field, args[field])
        return self.db.commit()

    def get_catalogs(self):
        return self.db.query(Catalog).order_by(Catalog.name)

    def backup_database(self):
        tables = (RequestList, Played, Song, Artist, Album, Mistags, Catalog)
        s = []
        for t in tables:
            s.append(dumps(self.db.query(t).all()))

        return s

    def is_updating(self):
        return False

