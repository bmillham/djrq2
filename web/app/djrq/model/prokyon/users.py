from . import *

class Users(Base):
    __tablename__ = 'users'

    uname = Column(String(50), primary_key=True)
    pword = Column(String(50))
