import sqlite3
import os
from time import sleep, time
from datetime import datetime

from ..model.prokyon.requestlist import RequestList
from ..model.prokyon.played import Played
from ..model.prokyon.mistags import Mistags
from ..model.prokyon.song import Song
from ..send_update import send_update

def backupdatabase(self):
    send_update(self.ws, progress=0, spinner=True, stage='Backup Creating backup database', updaterunning=True)

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
        send_update(self.ws, progress=0, spinner=True, stage='Backup: Getting Data To Backup for {}'.format(t.__name__))
        d = self._ctx.db.query(t)
        count = d.count()
        lp = 0
        lt = int(time())
        st = lt

        for i, r in enumerate(d):
            if i == 0:
                send_update(self.ws, spinner=False)

            cursor.execute(ti[t], r.__dict__)
            cp = int(i/count * 100)
            if lp != cp:
                lp = cp
                lt = int(time())
                percent = int(i/count * 100)
                send_update(self.ws, progress=percent, stage='Backing up {}'.format(t.__name__))
        db.commit()
    send_update(self.ws, spinner=False, stage='Backup Completed')
    db.close()
    updatedone = int(time())
    return True
