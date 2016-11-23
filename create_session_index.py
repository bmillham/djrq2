""" Run this one time, to setup the automatic expiration of sessions """

from web.app.djrq.model.session import Session
from pymongo import MongoClient

collection = MongoClient().djrq2.sessions

Session._expires.create_index(collection)
