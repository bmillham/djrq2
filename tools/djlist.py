from marrow.package.loader import load
from web.ext.djdb import DJDatabaseExtension
from web.ext.locale import LocaleExtension
from web.app.djrq.model.lastplay import DJs
import os
import sys

try:
    arghost = sys.argv[1]
except IndexError:
    arghost = os.uname()[1]

class FakeContext:
    """ A fake session, just used to query the database """
    def __init__(self, db={}, host=None, use_ssl=False):
        self.db = db
        self.queries = None
        self.__host = host
        if len(db) > 0:
            self.__djname = list(db.keys())[0]
        else:
            self.__djname = None
        self.use_ssl = use_ssl

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, db):
        self.__db=db

    @property
    def queries(self):
        return self.__queries

    @queries.setter
    def queries(self, queries):
        self.__queries = queries

    #@property
    #def catalogs(self):
    #    try:
    #        return self.__catalogs
    #    except:
    #        self.catalogs = [2,3]

    #@catalogs.setter
    #def catalogs(self, value):
    #    self.__catalogs = value

    @property
    def websocket(self):
        hn = self.__host
        if '.' not in hn:
            hn += '.local'
        return (f'{"https" if self.use_ssl else "http"}://'
                f'{self.__djname}.{hn}/pub?id={self.__djname}')
        

class DJInfo:
    def __init__(self, engines, djrow, site, use_ssl):
        self._engines = engines
        self.site = site
        self.real_djname = djrow.dj
        self.djname = djrow.dj.lower()
        self.databasetype = djrow.databasetype
        self.current_listeners = 0
        self.max_listeners = 0
        self.ignore_adj = djrow.ignore_adj
        self.db = self.engines[self.djname]
        self.context = FakeContext({self.djname: self.db.Session}, host=site, use_ssl=use_ssl)
        self.db.start(self.context)
        self.context.queries = self.queries(db=self.db.Session)
        self.context.listeners = self.listeners
        self.websocket = self.context.websocket
        self.use_ssl = use_ssl

    @property
    def websocket(self):
        return self._websocket

    @websocket.setter
    def websocket(self, ws):
        self._websocket = ws

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @property
    def engines(self):
        return self._engines

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, dbengine):
        self._db = dbengine
    
    @property
    def ignore_adj(self):
        return self._ignore_adj

    @ignore_adj.setter
    def ignore_adj(self, ignore):
        self._ignore_adj = ignore

    @property
    def djname(self):
        return self._djname

    @djname.setter
    def djname(self, djname):
        self._djname = djname

    @property
    def current_listeners(self):
        return self._current_listeners

    @current_listeners.setter
    def current_listeners(self, listeners):
        self._current_listeners = listeners

    @property
    def max_listeners(self):
        return self._max_listeners

    @max_listeners.setter
    def max_listeners(self, max_listeners):
        self._max_listeners = max_listeners

    @property
    def databasetype(self):
        return self._databasetype

    @databasetype.setter
    def databasetype(self, dbtype):
        self._databasetype = dbtype
        self.package = f'web.app.djrq.model.{dbtype}'

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, package):
        self._package = package
        self._queries = load(f'{package}.queries:Queries')
        self._listeners = load(f'{package}.listeners:Listeners')

    @property
    def queries(self):
        return self._queries

    @property
    def listeners(self):
        return self._listeners

class DJList:
    def __init__(self, config, site, use_ssl=False):
        self.context = FakeContext()
        self.site = site
        self.use_ssl = use_ssl
        self.databases = DJDatabaseExtension(config=config)
        self.lpdb = self.databases.engines['lastplay']
        self.lpdb.start(self.context)
        self.le = LocaleExtension()
        self._djs = {}
        self._get_djs()

    @property
    def djs(self):
        return self._djs

    def _get_djs(self):
        djlist = self.lpdb.Session.query(DJs).filter(DJs.hide_from_menu == 0)
        for djrow in djlist:
            print(f'Found DJ: {djrow.dj} {djrow.databasetype}')
            djname = djrow.dj.lower()
            djinfo = DJInfo(self.databases.engines, djrow, self.site, self.use_ssl)
            self._djs[djname] = djinfo

    def close_db(self):
        self.lpdb.Session.close()
        self.lpdb.stop(self.context)

