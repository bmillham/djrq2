from . import *

class Catalog(Base):
    __tablename__ = 'catalog'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    catalog_type = Column(String(128))
    last_update = Column(Integer)
    last_clean = Column(Integer)
    last_add = Column(Integer)
