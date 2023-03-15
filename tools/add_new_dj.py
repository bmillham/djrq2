# encoding: utf-8
# pip install sqlalchemy-utils
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy_utils.functions import create_database
from sqlalchemy.sql import select, insert

from web.app.djrq.model.lastplay import DJs
from web.app.djrq.model.lastplay import Base as DJBase

import yaml
import argparse
import scrypt
from os import urandom

parser = argparse.ArgumentParser(description='Add a new DJ to the djrq2 database')
parser.add_argument('dbtype', choices=['prokyon', 'ampache'], help='Database type to add')
parser.add_argument('-d', '--debug', action='store_true', help='Turn on debug messages')
parser.add_argument('-c', '--config_file', help='Use an alternate configuration file')
parser.add_argument('-j', '--dj', required=True, help='New DJ to add to the site_options')
parser.add_argument('-p', '--passwd', required=True, help='Password for a new DJ')
parser.add_argument('-u', '--server-user', required=True, help='Username for the database server')
parser.add_argument('-P', '--server-passwd', required=True,
                    help='Password for the database server')
parser.add_argument('-s', '--server', required=True, help='Database servername or IP')


args = parser.parse_args()

if not args.config_file:
    config_file = '../web/app/djrq/config.yaml'
else:
    config_file = args.config_file

if args.debug:
    print('Using config_file:', config_file)

if args.dbtype == 'prokyon':
    from web.app.djrq.model.prokyon import Base
    from web.app.djrq.model.prokyon.mistags import Mistags
    from web.app.djrq.model.prokyon.played import Played
    from web.app.djrq.model.prokyon.requestlist import RequestList
    from web.app.djrq.model.prokyon.siteoptions import SiteOptions
    from web.app.djrq.model.prokyon.song import Song
    from web.app.djrq.model.prokyon.suggestions import Suggestions
    from web.app.djrq.model.prokyon.users import Users
    from web.app.djrq.model.prokyon.listeners import Listeners
elif args.dbtype == 'ampache':
    from web.app.djrq.model.ampache import Base
    from web.app.djrq.model.ampache.mistags import Mistags
    from web.app.djrq.model.ampache.played import Played
    from web.app.djrq.model.ampache.requestlist import RequestList
    from web.app.djrq.model.ampache.siteoptions import SiteOptions
    from web.app.djrq.model.ampache.song import Song
    from web.app.djrq.model.ampache.suggestions import Suggestions
    from web.app.djrq.model.ampache.users import Users
    from web.app.djrq.model.ampache.listeners import Listeners

with open(config_file) as f:
    config= yaml.safe_load(f)

lpengine = create_engine('{uri}?charset=utf8'.format(**config['database']))
lpconn = lpengine.connect()

vals = {'dj': args.dj,
        'server': args.server,
        'password': args.server_passwd,
        'update_mine': 1,
        'update_others': 1,
        'ignore_adj': 1,
        'db': args.dj.lower(),
        'user': args.server_user,
        'auto_add': 1,
        'shout_title': f'DJ-{args.dj}',
        'hide_from_menu': 0,
        'databasetype': args.dbtype}
ins = insert(DJs).values(vals)
try:
    lpconn.execute(ins)
except Exception as e:
    print(f'Failed to add DJ: {e}')
    exit(1)

engine = create_engine(f"mysql://{vals['user']}:{vals['password']}@{vals['server']}/{args.dj.lower()}?charset=utf8",
                       echo=False)

print(f'Creating new database for {args.dj.lower()}')
create_database(engine.url)
Base.metadata.create_all(bind=engine)
db_created = True

vals = {'uname': args.dj.lower(),
        'administrator': True,
        'spword': scrypt.encrypt(str(urandom(64)), args.passwd, maxtime=0.5)}
print(f'Connecting to new database {args.dj.lower()}')
new_engine = engine.connect()
print(f'Inserting admin user {args.dj}')
ins = insert(Users).values(vals)
new_engine.execute(ins)
vals = {'show_title': '',
        'show_time': None,
        'limit_requests': 12,
        'offset': 0,
        'isupdating': 0,
        'isrestoring': 0}
print('Inserting default show options')
ins = insert(SiteOptions).values(vals)
new_engine.execute(ins)
new_engine.close()
print('Database created')
