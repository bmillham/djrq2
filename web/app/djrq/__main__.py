# encoding: utf-8

__import__('cinje')

import yaml
import os
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
from web.session.mongo import MongoSession
from web.ext.theme import ThemeExtension
from web.app.djrq.model.session import Session
from .root import Root

with open(os.path.join(os.path.dirname(__file__), 'config.yaml')) as f:
    config = yaml.safe_load(f)

app=Application(Root, extensions=[
        AnnotationExtension(),
        DebugExtension(),
        SerializationExtension(),
        DJHostExtension(),
        DJDatabaseExtension(sessions=MongoDBConnection(config['session']['uri']), lastplay_uri=config['database']['uri']),
        SelectiveDefaultDatabase(),
        DJExtension(),
        ThemeExtension(),
        SessionExtension(secret=config['session']['secret'],
                         expires=config['session']['expires'],
                         default=MongoSession(Session, database=config['session']['database']),
                         ),
        ] + ([DebugExtension(),] if __debug__ else []),
        )

if __name__ == "__main__":
    if __debug__:
        app.serve('wsgiref', host='0.0.0.0')
    else:
        app.serve('fcgi', socket=config['socket']['file'], umask=config['socket']['umask'])
