#! python
# Temporary script to correctly update last played info

import argparse

try:
    import pymysql
except ImportError:
    pymysql = False # So we know what module was used.
else:
    pymysql.install_as_MySQLdb()

try:
    import MySQLdb as sql
except ImportError:
    have_songdb = False
else:
    have_songdb = True


parser = argparse.ArgumentParser(description='Add missing played information to the database')
parser.add_argument('-u', '--user', required=True, help='The Database user')
parser.add_argument('-p', '--passwd', required=True, help='The Database password')
parser.add_argument('-d', '--database', required=True, help='Database to fix')
parser.add_argument('-s', '--server', default='localhost', help='Database servername or IP')
parser.add_argument('-o', '--port', type=int, default=3306, help='Database server port number')


args = parser.parse_args()

handle = sql.Connection(host=args.server, port=args.port, user=args.user, passwd=args.passwd,db=args.database)
cursor = handle.cursor()
cursor2 = handle.cursor()
inscurs = handle.cursor()

count = cursor.execute('select * from played')
print(f'Got {count} rows')
i = 0
for row in cursor.fetchall():
    i += 1
    #print(f'Song {row[1]}, Played {row[2].timestamp()}, Played by {row[3]}')
    exe = f'select * from object_count where date = {int(row[2].timestamp())} and object_id = {row[1]} and object_type="song"'
    #exe = f'select * from object_count where object_id = {row[1]} and object_type="song"'
    #print(exe)
    count = cursor2.execute(exe)
    #print(f'Got {count} rows {i}')
    if count > 0:
        continue
    try:
        user_info = row[3].split(' - ')
    except AttributeError:
        user_info = ['Unknown']
    usr = f"select * from user where fullname = %s"
    #print(usr)
    usrcount = inscurs.execute(usr, (user_info[0],))
    if usrcount == 0:
        print('no user', user_info[0])
        uins = f"insert into user (fullname, username, access) values (%s, %s, %s)"
        #print('insert', uins)
        inscurs.execute(uins, (user_info[0], user_info[0], 100))
        inscurs.execute(usr, (user_info[0],))
        irow = inscurs.fetchone()
        user_id = irow[0]
        #print('got user id', user_id)
    else:
        irow = inscurs.fetchone()
        #print(irow)
        user_id = irow[0]
    if 'bmillham' in user_info[0]:
        agent = 'IDJC:1'
    else:
        agent = 'IDJC:0'
    ins = f"insert into object_count (object_id, object_type, user, agent, date) values ({row[1]}, 'song', {user_id}, '{agent}', {int(row[2].timestamp())})"
    print(ins)
    inscount = inscurs.execute(ins)
    print(f'Inserted {row[2]} {inscount} rows {i}')
    upd = f"update song set played = 1 where id = {row[1]}"
    updcount = inscurs.execute(upd)
    #print(f'Updated {updcount} rows')

    
