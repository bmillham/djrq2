from . import *

class RequestList(Base):
    __tablename__= 'requestlist'
    __table_args__ = {'mysql_engine':'MyISAM'}
    id = Column('ID', Integer, primary_key=True)
    song_id = Column('songID', Integer, ForeignKey('tracks.id'), index=True)
    t_stamp = Column(DateTime, index=True)
    host = Column(String(255))
    msg = Column(String(255))
    name = Column(String(255))
    code = Column(Integer)
    eta = Column('ETA', DateTime)
    status = Column(Enum('played', 'ignored', 'pending', 'new','playing'), index=True)
