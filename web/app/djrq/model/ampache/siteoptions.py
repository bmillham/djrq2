from . import *

class SiteOptions(Base):
    __tablename__ = "site_options"
    id = Column(Integer, primary_key=True)
    show_title = Column(String(255))
    show_time = Column(String(255))
    show_end = Column(String(255))
    limit_requests = Column(String(255))
    offset = Column(Integer)
    catalog = Column(String(255))
