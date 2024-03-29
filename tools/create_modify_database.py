# pip install sqlalchemy-utils
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy_utils.functions import database_exists, create_database
from sqlalchemy.sql import select, insert

from web.app.djrq.model.lastplay import DJs
from web.app.djrq.model.lastplay import Base as DJBase

import yaml
import argparse
import hashlib
import scrypt
from os import urandom

parser = argparse.ArgumentParser(description='Create missing databases and add missing columns to tables')
parser.add_argument('dbtype', choices=['prokyon', 'ampache'], help='Database type to check')
parser.add_argument('-a', '--add_missing_columns', action='store_true', help='Add columns missing from the database')
parser.add_argument('--admin_user', help='Defines the site admin user for newly added databases')
parser.add_argument('--admin_passwd', help='Defines the site admin user password')
parser.add_argument('--add_missing_spw', action='store_true', help='Add missing scrypt password for admin user')
parser.add_argument('-d', '--debug', action='store_true', help='Turn on debug messages')
parser.add_argument('-c', '--config_file', help='Use an alternate configuration file')
parser.add_argument('-n', '--new-dj', help='New DJ to add to the site_options')
parser.add_argument('--new-dj-passwd', help='Password for a new DJ')

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
if not database_exists(lpengine.url):
    print(f"LP database {config['database']['uri']} does not exist, creating")
    create_database(lpengine.url)
    DJBase.metadata.create_all(bind=lpengine)
    lp = lpengine.connect()
    vals = {'dj': 'DJ-Bmillham',
            'server': 'eldrad.local',
            'password': '',
            'db': 'ampache1',
            'user': 'brian',
            'databasetype': 'ampache'}
    insert(DJs).values(vals)
    insert(DJs).values(dj='x', databasetype='ampache')
    lp.close()
    

lpconn = lpengine.connect()

if args.new_dj is not None:
    if args.new_dj_passwd is None:
        print('You must use the --new-dj-passwd option to set a password')
        exit(1)
    # Adding a new user
    vals = {'dj': args.new_dj.title(),
            'server': '10.8.0.1',
            'password': 'pgj399wq',
            'update_mine': 1,
            'update_others': 1,
            'ignore_adj': 1,
            'db': args.new_dj.lower(),
            'user': 'brian',
            'auto_add': 1,
            'shout_title': f'DJ-{args.new_dj.title()}',
            'hide_from_menu': 0,
            'databasetype': args.dbtype}
    ins = insert(DJs).values(vals)
    lpconn.execute(ins)

s = select([DJs]).where((DJs.hide_from_menu == 0) & (DJs.databasetype == args.dbtype))
results = lpconn.execute(s)

for row in results:

    db_created = False
    try:
        if row.server in config['database']['server_map']:
            dbserver = config['database']['server_map'][row.server]
        else:
            dbserver = row.server
    except KeyError:
        dbserver = row.server
        
    print('Checking if {} exists on {} ({})'.format(row.db, row.server, dbserver))
    engine = create_engine("mysql://{}:{}@{}/{}?charset=utf8".format(row.user, row.password, dbserver, row.db), echo=False)

    if not database_exists(engine.url):
        print(f'Creating new database for {args.new_dj}')
        create_database(engine.url)
        Base.metadata.create_all(bind=engine)
        db_created = True
        if args.new_dj_passwd:
            vals = {'uname': args.new_dj,
                    'administrator': True,
                    'spword': scrypt.encrypt(str(urandom(64)), args.new_dj_passwd, maxtime=0.5)}
            print(f'Connecting to new database {args.new_dj}')
            new_engine = engine.connect()
            print(f'Inserting admin user {args.new_dj}')
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


    Base.metadata.create_all(bind=engine)



    if args.add_missing_columns:
        print('Checking for missing columns')
        for table in (Mistags, Played, RequestList, SiteOptions, Song, Suggestions, Users, Listeners):
            meta = MetaData()
            print('Checking table {}'.format(table.__table__))
            u = Table(table.__table__, meta, autoload=True, autoload_with=engine)
            existing = [c.name for c in u.columns] # Get the columns in this table from the database
            if args.debug:
                print('Existing columns:', existing)
                print('ORM Columns:', table.__table__.columns)
            for col in table.__table__.columns:
                if col.name not in existing:
                    print('{} is missing in the database'.format(col.name))
                    cn = col.compile(dialect=engine.dialect)
                    ct = col.type.compile(dialect=engine.dialect)
                    sql = 'ALTER TABLE {} ADD COLUMN {} {}'.format(table.__table__, cn, ct)
                    if args.debug:
                        print('Executing: ', sql)
                    engine.execute(sql)

    if not args.admin_passwd:
        engine.dispose()
        continue

    spw = scrypt.encrypt(str(urandom(64)), args.admin_passwd, maxtime=0.5)
    #spw = scrypt.encrypt(urandom(64), args.admin_passwd, maxtime=0.5)
    us = select([Users.spword, Users.administrator]).where(Users.uname == args.admin_user)
    conn = engine.connect()
    res = conn.execute(us).fetchone()
    if res is None or db_created:
        print('Creating admin user')
        admin_user = Users.__table__.insert().values(uname=args.admin_user,
                                                     pword=hashlib.md5(args.admin_passwd.encode()).hexdigest(),
                                                     spword=spw,
                                                     administrator=True)
        engine.execute(admin_user)
        res = conn.execute(us).fetchone()

    if res.spword is None and args.add_missing_spw:
        add_spw = Users.__table__.update().where(Users.uname == args.admin_user).values(spword=spw)
        conn.execute(add_spw)
        res = conn.execute(us).fetchone()

    if res.administrator is None:
        add_admin = Users.__table__.update().where(Users.uname == args.admin_user).values(administrator=True)
        conn.execute(add_admin)
    try:
        y = scrypt.decrypt(res.spword, args.admin_passwd, maxtime=1)
    except scrypt.error:
        print('The password set in the database does not match the given password.')
    except TypeError:
        print('The password was not set in the database')
    else:
        print('Password matches')
