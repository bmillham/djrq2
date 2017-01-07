from . import *

from sqlalchemy import Text

class Mistags(Base):
    __tablename__ = 'mistags'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('tracks.id'))
    reported_by = Column(Text)
    reported = Column(DateTime, server_default=func.now())
    artist = Column(Text)
    album = Column(Text)
    title = Column(Text)
    comments = Column(String(2000))
