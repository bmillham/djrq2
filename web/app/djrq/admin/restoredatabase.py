import sqlite3
import os
from time import sleep, time
from datetime import datetime

from ..model.prokyon.requestlist import RequestList
from ..model.prokyon.played import Played
from ..model.prokyon.mistags import Mistags
from ..model.prokyon.song import Song
from ..send_update import send_update

class RestoreDatabase:
    __dispatch__ = 'resource'
    __resource__ = 'restoredatabase'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        ctx = context
        self.uploaddir = os.path.join('privatefilearea', context.djname)
        self.ws = context.websocket_admin

    def get(self, *arg, **args):
        return self.restoredatabase()

    def restoredatabase(self):
        #send_update(self.ws, progress=0, spinner=True, stage='Backup Creating backup database', updaterunning=True)

        db = sqlite3.connect(os.path.join(self.uploaddir, 'dbbackup20170124-052742'))
        cursor = db.cursor()
        #tables = (Song, RequestList, Played, Mistags)
        keys = {Song: ['id', 'title', 'artist_fullname', 'album_fullname', 'path', 'filename', 'year', 'bit_rate', 'sample_rate', 'time', 'track', '_addition_time', 'size'],
                RequestList: ['id', 'song_id', 't_stamp', 'host', 'msg', 'name', 'code', 'eta', 'status'],
                Played: ['played_id', 'track_id', 'date_played', 'played_by', 'played_by_me'],
                Mistags: ['id', 'track_id', 'reported_by', 'reported', 'artist', 'album', 'title', 'comments']
               }
        tc = {Song: 'SELECT * FROM tracks',
              RequestList: 'SELECT * FROM requestlist',
              Played: 'SELECT * FROM played',
              Mistags: 'SELECT * FROM mistags'
             }
        tables = (Song, RequestList, Played, Mistags)
        updatestart = int(time())
        for t in tables:
            tstart = int(time())
            print('Working on', t)
            d = cursor.execute(tc[t])
            self._ctx.db.query(t).delete()
            #db.commit()
            #send_update(self.ws, progress=0, spinner=True, stage='Backup: Getting Data To Backup for {}'.format(t.__name__))
            #d = self._ctx.db.query(t)
            #count = d.count()
            #lp = 0
            #lt = int(time())
            #st = lt

            for i, r in enumerate(d):
                row = dict(zip(keys[t], r))
                if t is Song:
                    row['jingle'] = 0
                #print(row)
                nr = t(**row)
                self._ctx.db.add(nr)

                #print(row)
                #if i == 0:
                #    send_update(self.ws, spinner=False)

                #cursor.execute(ti[t], r.__dict__)
                #cp = int(i/count * 100)
                #if lp != cp:
                #    lp = cp
                #    lt = int(time())
                #    percent = int(i/count * 100)
                #    send_update(self.ws, progress=percent, stage='Backing up {}'.format(t.__name__))
            #db.commit()
            tend = int(time())
            print('Rows added in', tend - tstart, 'commiting')
            self._ctx.db.commit() # Must commit to get the id
            print('Commited', int(time()) - tend)

        #send_update(self.ws, spinner=False, stage='Backup Completed')

        db.close()
        updatedone = int(time())
        print('Update took', updatedone - updatestart)
        return True

