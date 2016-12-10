import sqlite3
import os
from time import sleep, time
from datetime import datetime
import requests
import json

from ..model.prokyon.requestlist import RequestList
from ..model.prokyon.played import Played
from ..model.prokyon.mistags import Mistags
from ..model.prokyon.song import Song

def backupdatabase(self):
    db = sqlite3.connect(os.path.join(self.uploaddir, 'dbbackup{}'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))))
    cursor = db.cursor()
    tables = (Song, RequestList, Played, Mistags)
    tc = {RequestList: 'create table requestlist(id INTEGER PRIMARY KEY, song_id INTEGER, t_stamp DATETIME, host TEXT, msg TEXT, name TEXT, code TEXT, eta DATETIME, status TEXT)',
          Played: 'CREATE TABLE played(played_id INTEGER, track_id INTEGER, date_played DATETIME, played_by TEXT, played_by_me INTEGER)',
          Mistags: 'CREATE TABLE mistags(id INTEGER PRIMARY KEY, track_id INTEGER, reported_by TEXT, reported DATETIME, artist TEXT, album TEXT, title TEXT, comments TEXT)',
          Song: 'CREATE TABLE tracks(id INTEGER PRIMARY KEY, title TEXT, artist TEXT, album TEXT, path TEXT, filename TEXT, year TEXT, bitrate INTEGER, samplerate INTEGER, length INTEGER, tracknumber INTEGER, lastModified DATETIME, size INTEGER)',
         }
    ti = {RequestList: 'INSERT INTO requestlist(id, song_id, t_stamp, host, msg, name, code, eta, status) values (:id, :song_id, :t_stamp, :host, :msg, :name, :code, :eta, :status)',
          Played: 'INSERT INTO played(played_id, track_id, date_played, played_by, played_by_me) values(:played_id, :track_id, :date_played, :played_by, :played_by_me)',
          Mistags: 'INSERT INTO mistags(id, track_id, reported_by, reported, artist, album, title, comments) values(:id, :track_id, :reported_by, :reported, :artist, :album, :title, :comments)',
          Song: 'INSERT INTO tracks(id, title, artist, album, path, filename, year, bitrate, samplerate, length, tracknumber, lastModified, size) values(:id, :title, :artist_fullname, :album_fullname, :path, :filename, :year, :bit_rate, :sample_rate, :time, :track, :_addition_time, :size)',
         }
    updatestart = int(time())
    for t in tables:
        cursor.execute(tc[t])
        db.commit()
        print('Getting data to backup')
        d = {'progress': 0,
             'stage': 'Backup: Getting Data To Backup for {}'.format(t.__name__)}
        r = requests.post(self.ws, data=json.dumps(d))
        d = self._ctx.db.query(t)
        count = d.count()
        print('Backing up: ', d.count())
        lp = 0
        lt = int(time())
        print('Start time', lt)
        st = lt
        for i, r in enumerate(d):
            if i == 0:
                print('Loop start:', int(time()))
            #i += 1
            cursor.execute(ti[t], r.__dict__)
            cp = int(i/count * 100)
            if lp != cp:
            #if int(time()) > lt + 1:
            #if i % 10 == 0:
                lp = cp
                lt = int(time())
                #print('update', lt)
                percent = int(i/count * 100)
                d = {'stage': 'Backing up {}'.format(t.__name__),
                     'progress': percent}
                r = requests.post(self.ws, data=json.dumps(d))
        print('Done:', int(time()), int(time()) - st)
        db.commit()
        print('Done with table')
    db.close()
    updatedone = int(time())
    print("UPdate time:", updatedone - updatestart)
    return True