from . import *
from .song import Song
from .album import Album
from .artist import Artist

class Played(Base):
    __tablename__ = 'played'
    __table_args__ = {'mysql_engine':'MyISAM'}
    played_id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('song.id'))
    date_played = Column(DateTime)
    played_by = Column(String(255))
    played_by_me = Column(Integer)

	# TODO: This doesn't work right now. Kept for now until I decide what to do
    def get_multi_albums(self):
        return session.query(Song).join(Album).join(Artist).filter(Artist.fullname == self.song.artist.fullname, Song.title == self.song.title)

