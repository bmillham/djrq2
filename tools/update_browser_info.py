# encoding: utf8

# Temporary script to update the users browser listeners and played info

import cinje
from web.core import Application
from marrow.package.loader import load
from web.ext.djdb import DJDatabaseExtension
from web.ext.dj import DJExtension
from web.app.djrq.model.lastplay import DJs
from web.app.djrq.send_update import send_update
from web.app.djrq.templates.lastplayed import lastplayed_row
from sqlalchemy.sql import func
from time import sleep
import yaml

class FakeContext:
    """ A fake session, just used to query the database """
    def __init__(self, db={}):
        self.db = db
        self.queries = None

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

with open('../web/app/djrq/config.yaml') as f:
    config= yaml.safe_load(f)

if __name__ == '__main__':
    databases = DJDatabaseExtension(config=config)
    lp = databases.engines['lastplay']
    context = FakeContext()
    lp.start(context)
    l = lp.Session.query(DJs).filter(DJs.hide_from_menu == 0)
    djs = {}
    for djrow in l:
        package = 'web.app.djrq.model.'+djrow.databasetype
        djname = djrow.dj.lower()
        djs[djname] = {'databasetype': djrow.databasetype,
                    'package': 'web.app.djrq.model.'+djrow.databasetype,
                    'lp_id': None,
                    'current_listeners': 0,
                    'current_max_listeners': 0,
                    'queries': load(package + '.queries:Queries'),
                    'listeners': load(package + '.listeners:Listeners'),
                    'websocket': 'http://{}.rockitradio.info/pub?id={}'.format(djname, djname),
                    }
        #djs[djname]['websocket'] = 'http://dj-{}.gelth.local/pub?id=dj-{}'.format(djname, djname)

    lp.Session.close()
    lp.stop(context)

    while 1:
        # Get the latest played for each DJ
        for dj in databases.engines:
            elements_to_update = {}
            if dj == 'lastplay': continue

            db = databases.engines[dj]
            context = FakeContext()
            db.start(context)
            queries = djs[dj]['queries'](db=db.Session)
            context.queries = queries

            try:
                lp = queries.get_last_played(count=1)
            except:
                print("No lastplay for {}".format(dj))
            else:
                try:
                    r = lp[0]
                except:
                    #print('Bad row', dj)
                    continue

                if r[0] == 0: continue
                print('r', r[0], r)
                if djs[dj]['lp_id'] is None:
                    for rq in r.Played.song.new_requests:
                        print(rq.id, rq.msg, rq.name)
                        elements_to_update['request_id'] = rq.id
                        elements_to_update['new_request_status'] = 'played'
                    djs[dj]['lp_id'] = r.Played.played_id
                elif r.Played.played_id == djs[dj]['lp_id']:
                    pass # Skip if no change
                else:
                    new_row = cinje.flatten(lastplayed_row(context, r, ma=True, played=True))
                    for rq in r.Played.song.new_requests:
                        #print(rq.id, rq.msg, rq.name)
                        elements_to_update['request_id'] = rq.id
                        elements_to_update['new_request_status'] = 'played'
                    elements_to_update['lastplay'] = new_row
                    djs[dj]['lp_id'] = r.Played.played_id
            try:
                listeners_row = db.Session.query(djs[dj]['listeners']).one()
            except:
                pass # Skip because no listeners info
            else:
                if listeners_row.current != djs[dj]['current_listeners']:
                    djs[dj]['current_listeners'] = listeners_row.current
                    elements_to_update['listeners'] = listeners_row.current
                if listeners_row.max != djs[dj]['current_max_listeners']:
                    djs[dj]['current_max_listeners'] = listeners_row.max
                    elements_to_update['maxlisteners'] = listeners_row.max

            if elements_to_update != {}:
                print('Sending update to', djs[dj]['websocket'], elements_to_update)
                send_update(djs[dj]['websocket'], **elements_to_update)
            db.Session.close()
            db.stop(context)
        sleep(10)
