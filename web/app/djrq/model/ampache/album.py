from . import *
from sqlalchemy.sql import case
from sqlalchemy.orm import column_property

class Album(Base):
	__tablename__ = 'album'
	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	prefix = Column(String(32))
	year = Column(Integer)
	disk = Column(SmallInteger)
	Index(name)
	Index(prefix)
	__table_args__ = {'mysql_engine':'MyISAM'}

	#def __str__(self):
	#	return u'<a href="/album/?id={}">{}</a>'.format(self.id, self.fullname)

	#def get_url(self):
	#	return "/album/?id={}".format(self.id)

	@hybrid_property
	def fullname(self):
		name = []
		if self.prefix is not None:
			name.append(self.prefix)
		name.append(self.name)
		if self.disk is not None and self.disk != 0:
			name.append("[Disc {}]".format(self.disk))
		if self.year is not None and self.year != 0:
			name.append("({})".format(self.year))
		return " ".join(name)

	@fullname.expression
	def fullname(self):
		return func.concat_ws(" ", self.prefix, self.name,
			case([
				(self.disk != 0, func.concat("[Disk ",self.disk,"]")),
				],),
			case([(self.year != 0, func.concat("(", self.year, ")")),],
				))

Album.fullname_url = column_property(func.concat('<a href="/album/?id=', Album.id, '">', Album.fullname, '</a>'))
	
