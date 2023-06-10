from . import *

class ObjectCount(Base):
    __tablename__ = 'object_count'
    __table_args__ = {'mysql_engine':'MyISAM'}
    id = Column(Integer, primary_key=True)
    object_type = Column(Enum('album', 'artist', 'song', 'playlist', 'genre', 'catalog', 'live_stream', 'video'))
    object_id = Column(Integer)
    date = Column(Integer)
    user = Column(Integer)
    agent = Column(String(255))

