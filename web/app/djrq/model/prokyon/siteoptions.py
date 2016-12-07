from . import *

class SiteOptions(Base):
    __tablename__ = "site_options"
    id = Column(Integer, primary_key=True)
    show_title = Column(String(255))
    show_time = Column(String(255))
    show_end = Column(String(255))
    limit_requests = Column(String(255))
    offset = Column(Integer)
    isupdating = Column(Boolean)

    @hybrid_property
    def catalog(self):
        return "1"

    @catalog.expression
    def catalog(self):
        return '1'

    @property
    def catalog(self):
        return "1"
