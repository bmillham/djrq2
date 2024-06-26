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

    def __init__(self, default=None, sessions=None, config=None):
        self.needs = set(self._needs)
        self.provides = set(self._provides)

        engines = {'lastplay': SQLAlchemyConnection(config['database']['uri'])}
        context = FakeContext()
        engines['lastplay'].start(context)
        djs = engines['lastplay'].Session.query(DJs).filter(DJs.hide_from_menu == 0)

        for d in djs:
            # Use the server_map to redirect database server located in the lastplay database
            try:
                server = config['database']['server_map'][d.server] if d.server in config['database']['server_map'].keys() else d.server
            except KeyError:
                server = d.server
            url = "mysql://{}:{}@{}/{}?charset=utf8mb4".format(d.user, d.password, server, d.db)
            engines[d.dj.lower()] = SQLAlchemyConnection(url)

        engines['lastplay'].stop(context)
        if sessions:
            engines['sessions'] = sessions
        super(DJDatabaseExtension, self).__init__(default, **engines)
