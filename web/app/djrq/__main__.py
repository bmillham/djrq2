# encoding: utf-8

__import__('cinje')

from web.core import Application
from web.ext.annotation import AnnotationExtension
from web.ext.debug import DebugExtension
from web.ext.serialize import SerializationExtension
from web.ext.djdb import DJDatabaseExtension
from web.ext.selective import SelectiveDefaultDatabase
from web.ext.dj import DJExtension
from web.ext.djhost import DJHostExtension
from web.ext.db import DatabaseExtension
from web.db.mongo import MongoDBConnection
from web.ext.session import SessionExtension
from web.session.mongo import MongoSession, MongoSessionStorage
from marrow.mongo.core import Field
from marrow.mongo import String

from .root import Root

SESSION_URI = 'mongodb://localhost/djrq2'
SESSION_SECRET = 'xyzzy'

class Session(MongoSessionStorage):
    __collection__ = 'sessions'

    username = String(default=None)
    sitenick = String(default=None)
    #usertheme = String(default=None)

app=Application(Root, extensions=[
        AnnotationExtension(),
        DebugExtension(),
        SerializationExtension(),
        DJHostExtension(),
        DJDatabaseExtension(sessions=MongoDBConnection(SESSION_URI)),
        SelectiveDefaultDatabase(),
        DJExtension(),
        SessionExtension(secret=SESSION_SECRET,
                         expires=24*90,
                         default=MongoSession(Session, database='sessions'),
                         ),
        ])

if __name__ == "__main__":
    app.serve('wsgiref', host='0.0.0.0')
