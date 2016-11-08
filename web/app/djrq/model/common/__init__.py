from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.sql import func, or_
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class Listeners(Base):
    __tablename__ = "listeners"

    id = Column(Integer, primary_key=True)
    current = Column(Integer)
    max = Column(Integer)
