# encoding: utf-8
# pip install sqlalchemy-utils
from sqlalchemy import create_engine
from sqlalchemy.sql import update

import argparse
import scrypt
from os import urandom

parser = argparse.ArgumentParser(description='Change a DJs password')
parser.add_argument('dbtype', choices=['prokyon', 'ampache'], help='Database type for the DJ')
parser.add_argument('-j', '--dj', required=True, help='The DJ to change password for')
parser.add_argument('-p', '--passwd', required=True, help='New Password for the DJ')
parser.add_argument('-u', '--server-user', required=True, help='Username for the database server')
parser.add_argument('-P', '--server-passwd', required=True,
                    help='Password for the database server')
parser.add_argument('-s', '--server', required=True, help='Database servername or IP')


args = parser.parse_args()

if args.dbtype == 'prokyon':
    from web.app.djrq.model.prokyon.users import Users
elif args.dbtype == 'ampache':
    from web.app.djrq.model.ampache.users import Users

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
