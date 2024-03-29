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
from web.ext.acl import ACLExtension, when
from web.ext.auth import AuthExtension
from web.ext.locale import LocaleExtension
from web.ext.git import GitExtension
from web.db.mongo import MongoDBConnection
from web.ext.session import SessionExtension
from web.session.mongo import MongoSession
from web.ext.theme import ThemeExtension
from web.app.djrq.model.session import Session
from web.app.djrq.admin.auth import Auth
from datetime import timedelta
import time
from .root import Root
import git

with open(os.path.join(os.path.dirname(__file__), 'config.yaml')) as f:
    config = yaml.safe_load(f)



app=Application(Root, extensions=[
        AnnotationExtension(),
        SerializationExtension(),
        GitExtension(),
        DJHostExtension(),
        DJDatabaseExtension(sessions=MongoDBConnection(config['session']['uri']), config=config),
        SelectiveDefaultDatabase(),
        DJExtension(config=config['site']),
        ThemeExtension(default=config['site']['default_theme']),
        ACLExtension(default=when.always),
        AuthExtension(intercept=None, name=None, session='authenticated', lookup=Auth.lookup, authenticate=Auth.authenticate),
        SessionExtension(secret=config['session']['secret'],
                         expires=timedelta(days=config['session']['expires']),
                         refresh=True,
                         default=MongoSession(Session, database=config['session']['database']),
                         ),
        LocaleExtension(),
        ] + ([DebugExtension(),] if __debug__ else []),

        )

if __name__ == "__main__":
    if __debug__:
        app.serve('wsgiref', host='0.0.0.0', port=8888)
    else:
        app.serve('fcgi', socket=config['socket']['file'], umask=config['socket']['umask'])
