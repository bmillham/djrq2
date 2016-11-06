from . import *

class Suggestions(Base):
    __tablename__ = 'suggestions'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    album = Column(String(255))
    artist = Column(String(255))
    suggestor = Column(String(255))
    comments = Column(String(255))
