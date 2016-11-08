from . import *

class Catalog(Base):
    __tablename__ = "cc_music_dirs"
    id = Column(Integer, primary_key=True)
    directory = Column(String)
    type = Column(String(255))
    exists = Column(Boolean)
    watched = Column(Boolean)

    @hybrid_property
    def name(self):
        return self.directory.rsplit('/', 2)[1]
