from . import *

class Album(Base):
    __tablename__ = "album_view"

    id = Column(Integer, primary_key=True)
    fullname = Column(Text)
    name = Column(Text)
    prefix = Column(Text)
