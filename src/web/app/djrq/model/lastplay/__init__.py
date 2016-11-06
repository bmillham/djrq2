from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.sql import func, or_


Base = declarative_base()

class DJs(Base):
    __tablename__ = 'update_options'
    dj = Column(String(50), primary_key=True)
    server = Column(Text())
    password = Column(Text())
    update_mine = Column(Integer())
    update_others = Column(Integer())
    ignore_adj = Column(Integer())
    db = Column(Text())
    user = Column(Text())
    auto_add = Column(Integer())
    shout_title = Column(Text())
    hide_from_menu = Column(Integer())
    databasetype = Column(Enum('prokyon', 'sam', 'ampache'))
