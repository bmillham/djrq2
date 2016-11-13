from web.session.mongo import MongoSessionStorage
from marrow.mongo import String

class Session(MongoSessionStorage):
    __collection__ = 'sessions'

    username = String(default=None)
    sitenick = String(default=None)
    usertheme = String(default='United')
    #usertheme = String(default=None)
