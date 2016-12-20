from . import *
from sqlalchemy.orm import column_property

class Artist(Base):
    __tablename__ = 'artist'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    prefix = Column(String(32))
    Index(name)
    Index(prefix)

    __table_args__ = {'mysql_engine':'MyISAM'}

    def __str__(self):
        return u'<a href="/artist/?id={}">{}</a>'.format(self.id, self.fullname)

    @property
    def new_link(self):
        return u'<a href="/artist/new/{}">{}</a>'.format(self.id, self.fullname)

    def get_url(self):
        return "/artist/{}".format(self.id)

    @hybrid_property
    def fullname(self):
        if self.prefix is None:
            return self.name
        else:
            return self.prefix + " " + self.name

    @fullname.expression
    def fullname(self):
        return func.concat_ws(" ", self.prefix, self.name)

Artist.fullname_url = column_property(func.concat('<a href="/artist/?id=', Artist.id, '">', Artist.fullname, '</a>'))
