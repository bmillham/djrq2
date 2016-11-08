from . import *

class Mistags(Base):
    __tablename__ = 'mistags'
    __table_args__ = {'mysql_engine':'MyISAM'}
    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('song.id'))
    reported_by = Column(String(255))
    reported = Column(TIMESTAMP)
    artist = Column(String(255))
    album = Column(String(255))
    title = Column(String(255))
    comments = Column(String(255))
