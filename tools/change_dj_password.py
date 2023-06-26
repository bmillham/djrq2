# encoding: utf-8
# pip install sqlalchemy-utils
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, insert, update

import yaml
import argparse
import scrypt
from os import urandom

parser = argparse.ArgumentParser(description='Change a DJs password')
parser.add_argument('dbtype', choices=['prokyon', 'ampache'], help='Database type to add')
parser.add_argument('-d', '--debug', action='store_true', help='Turn on debug messages')
parser.add_argument('-c', '--config_file', help='Use an alternate configuration file')
parser.add_argument('-j', '--dj', required=True, help='The DJ to change password')
parser.add_argument('-p', '--passwd', required=True, help='New Password for the new DJ')
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

with open(config_file) as f:
    config= yaml.safe_load(f)

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
    index_list = {'tracks': ('artist', 'album', 'title')}
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

engine = create_engine(f"mysql://{args.server_user}:{args.server_passwd}@{args.server}/{args.dj.lower()}?charset=utf8",
                       echo=False)

print(f'Connecting to database database {args.dj.lower()}')
new_engine = engine.connect()
print(f'Updating DJ {args.dj} password')
upd = update(Users).filter(Users.uname == args.dj.lower()).\
          values({'spword': scrypt.encrypt(str(urandom(64)), args.passwd, maxtime=0.5)})
new_engine.execute(upd)

new_engine.close()
print('Password changed')
