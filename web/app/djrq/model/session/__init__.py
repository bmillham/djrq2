from web.session.mongo import MongoSessionStorage
from marrow.mongo import Index
from marrow.mongo.field import String, TTL
from datetime import timedelta

class Session(MongoSessionStorage):
    __collection__ = 'sessions'

    username = String(default=None)
    sitenick = String(default=None)
    usertheme = String(default=None)
    expires = TTL(default=timedelta(days=365), assign=True)
    _expires = Index('expires', expire=0)

