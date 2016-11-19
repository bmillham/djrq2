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
from web.ext.acl import ACLExtension, when
from web.ext.auth import AuthExtension
from web.db.mongo import MongoDBConnection
from web.ext.session import SessionExtension
from web.session.mongo import MongoSession
from web.ext.theme import ThemeExtension

from web.app.djrq.model.session import Session

from .root import Root

SESSION_URI = 'mongodb://localhost/djrq2'
SESSION_SECRET = 'xyzzy'

app=Application(Root, extensions=[
        AnnotationExtension(),
        DebugExtension(),
        SerializationExtension(),
        ACLExtension(default=when.always),
        AuthExtension(),
        DJHostExtension(),
        DJDatabaseExtension(sessions=MongoDBConnection(SESSION_URI)),
        SelectiveDefaultDatabase(),
        DJExtension(),
        ThemeExtension(),
        SessionExtension(secret=SESSION_SECRET,
                         expires=24*90,
                         default=MongoSession(Session, database='sessions'),
                         ),
        ] + ([DebugExtension(),] if __debug__ else []),
        )

if __name__ == "__main__":
    if __debug__:
        app.serve('wsgiref', host='0.0.0.0')
    else:
        app.serve('fcgi', socket='/home/brian/djrq2-workingcopy/djrq2/var/djrq2-1.sock', umask=000)
