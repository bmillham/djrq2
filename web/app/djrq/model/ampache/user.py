from . import *

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True)
    fullname = Column(String(128))
    email = Column(String(128))
    website = Column(String(255))
    apikey = Column(String(255))
    password = Column(String(128))
    access = Column(Integer)
    disabled = Column(Boolean)
    last_seen = Column(Integer)
    create_date = Column(Integer)
    validation = Column(String(128))

