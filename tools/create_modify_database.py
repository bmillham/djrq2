# pip install sqlalchemy-utils
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy_utils.functions import database_exists, create_database
from sqlalchemy.sql import select

from web.app.djrq.model.lastplay import DJs

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

args = parser.parse_args()

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

with open('../web/app/djrq/config.yaml') as f:
    config= yaml.safe_load(f)

lpengine = create_engine('{uri}?charset=utf8'.format(**config['database']))
lpconn = lpengine.connect()
s = select([DJs]).where((DJs.hide_from_menu == 0) & (DJs.databasetype == args.dbtype))
results = lpconn.execute(s)

for row in results:
    print('Checking if {db} exists on {server}'.format(**row))
    db_created = False
    engine = create_engine("mysql://{user}:{password}@{server}/{db}?charset=utf8".format(**row), echo=False)

    if not database_exists(engine.url):
        print('Creating {}'.format(engine.url))
        create_database(engine.url)
        db_created = True

    Base.metadata.create_all(bind=engine)

    spw = scrypt.encrypt(str(urandom(64)), args.admin_passwd, maxtime=0.5)
    #spw = scrypt.encrypt(urandom(64), args.admin_passwd, maxtime=0.5)

    if db_created:
        admin_user = Users.__table__.insert().values(uname=args.admin_user,
                                                     pword=hashlib.md5(args.admin_passwd.encode()).hexdigest(),
                                                     spword=spw,
                                                     administrator=True)
        engine.execute(admin_user)

    if args.add_missing_columns:
        print('Checking for missing columns')
        for table in (Mistags, Played, RequestList, SiteOptions, Song, Suggestions, Users, Listeners):
            meta = MetaData()
            print('Checking table {}'.format(table.__table__))
            u = Table(table.__table__, meta, autoload=True, autoload_with=engine)
            existing = [c.name for c in u.columns] # Get the columns in this table from the database
            for col in table.__table__.columns:
                if col.name not in existing:
                    print('{} is missing in the database'.format(col.name))
                    cn = col.compile(dialect=engine.dialect)
                    ct = col.type.compile(dialect=engine.dialect)
                    sql = 'ALTER TABLE {} ADD COLUMN {} {}'.format(table.__table__, cn, ct)
                    engine.execute(sql)

    us = select([Users.spword, Users.administrator]).where(Users.uname == args.admin_user)
    conn = engine.connect()
    res = conn.execute(us).fetchone()
    if res.spword is None and args.add_missing_spw:
        add_spw = Users.__table__.update().where(Users.uname == args.admin_user).values(spword=spw)
        conn.execute(add_spw)
        res = conn.execute(us).fetchone()

    if res.administrator is None:
        add_admin = Users.__table__.update().where(Users.uname == args.admin_user).values(administrator=True)
        conn.execute(add_admin)
    try:
        y = scrypt.decrypt(res.spword, args.admin_passwd, maxtime=0.5)
    except scrypt.error:
        print('The password set in the database does not match the given password.')
    except TypeError:
        print('The password was not set in the database')
    else:
        print('Password matches')
