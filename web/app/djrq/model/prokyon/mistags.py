from . import *

class Mistags(Base):
    __tablename__ = 'mistags'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('tracks.id'))
    reported_by = Column(String)
    reported = Column(DateTime, server_default=func.now())
    artist = Column(String)
    album = Column(String)
    title = Column(String)
    comments = Column(String)
