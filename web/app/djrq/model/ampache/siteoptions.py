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
    auto_update_requests = Column(Boolean, default=False)
    metadata_fields = Column(Enum('artist - title', 'artist - title - album'),
                       default='artist - title - artist')
    strict_metadata = Column(Boolean, default=True)
    played_reporting_fields = Column(Enum('dj', 'dj - show title', 'show title'),
                                     default='dj')


