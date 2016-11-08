from . import *
from .song import Song

class Played(Base):
    __tablename__ = 'played'
    __table_args__ = {'mysql_engine':'MyISAM'}
    played_id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('tracks.id'))
    date_played = Column(DateTime)
    played_by = Column(String(255))
    played_by_me = Column(Integer)

#    def get_multi_albums(self):
#        return session.query(Song).filter(Song.fullname == self.song.artist.fullname, Song.title == self.song.title)

