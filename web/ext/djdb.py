from web.ext.db import DatabaseExtension
from web.db.sa import SQLAlchemyConnection
from web.app.djrq.model.lastplay import DJs


class FakeContext:
    """ A fake session, just used to query the database """
    def __init__(self):
        self.db = {}

class DJDatabaseExtension(DatabaseExtension):
    _needs = {'djhost'}
    _provides = {'djdb', 'db'}

    def __init__(self, default=None, sessions=None, lastplay_uri=None):
        self.needs = set(self._needs)
        self.provides = set(self._provides)

        engines = {'lastplay': SQLAlchemyConnection(lastplay_uri)}
        context = FakeContext()
        engines['lastplay'].start(context)
        djs = engines['lastplay'].Session.query(DJs).filter(DJs.hide_from_menu == 0)

        for d in djs:
            # TODO: make this configurable
            server = "themaster.millham.net" if d.server == "localhost" else d.server
            url = "mysql://{}:{}@{}/{}?charset=utf8".format(d.user, d.password, server, d.db)
            engines[d.dj.lower()] = SQLAlchemyConnection(url)
            print(d.user, d.db, server)

        engines['lastplay'].stop(context)
        if sessions:
            engines['sessions'] = sessions
        super(DJDatabaseExtension, self).__init__(default, **engines)
