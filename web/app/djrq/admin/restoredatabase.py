# encoding: utf-8

import sqlite3
import os
import sys
from time import sleep, time
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

from ..model.prokyon.requestlist import RequestList
from ..model.prokyon.played import Played
from ..model.prokyon.mistags import Mistags
from ..model.prokyon.song import Song
from ..send_update import send_update
from ..templates.admin.updatehistory import selectfile
from ..templates.admin.updatedatabase import restoreprogress
from glob import glob
from concurrent.futures import ThreadPoolExecutor

class RestoreDatabase:
    __dispatch__ = 'resource'
    __resource__ = 'restoredatabase'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        ctx = context
        self.uploaddir = os.path.join('privatefilearea', context.djname)
        self.ws = context.websocket_admin

    def get(self, *arg, **args):
        if self._ctx.queries.is_updating():
            return selectdatabasefile('Updating Database', self._ctx)
        if self._ctx.queries.is_restoring():
            return restoreprogress('Restoring Database', self._ctx)
        files = sorted(glob(os.path.join(self.uploaddir, 'dbbackup-*.sqlite')), reverse=True)
        return selectfile("Select Backup File", self._ctx, files, action='/admin/restoredatabase')

    def post(self, *arg, **args):
        self._ctx.queries.is_restoring(status=True)
        url = self._ctx.db[self._ctx.djname.lower()].session_factory.__dict__['kw']['bind'].url
        self.executor = ThreadPoolExecutor(max_workers=1)
        future = self.executor.submit(self._restoredatabase, url=url, fileselection=args['fileselection'])
        future.add_done_callback(self._restorecomplete)
        return restoreprogress('Restoring Database', self._ctx)

    def _restorecomplete(self, future):
        self._ctx.queries.is_restoring(status=False)
        self.executor.shutdown(wait=False)
        return True

    def _restoredatabase(self, *arg, **args):
        send_update(self.ws, progress=0, spinner=True, stage='Starting Database Restore', updaterunning=True)

        db = sqlite3.connect(os.path.join(self.uploaddir, args['fileselection']))
        cursor = db.cursor()
        try:
            engine = create_engine(args['url'])
        except:
            print('Failed to create engine', sys.exc_info())
        conn = engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()

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
        counts = {Song: 'SELECT COUNT(*) FROM tracks',
                  RequestList: 'SELECT COUNT(*) FROM requestlist',
                  Played: 'SELECT COUNT(*) FROM played',
                  Mistags: 'SELECT COUNT(*) FROM mistags',
                 }
        tables = (Song, RequestList, Played, Mistags)
        realstarttime = int(time())
        send_args = {}

        for t in tables:
            t_name = t.__name__
            tstart = int(time())
            send_update(self.ws, r_progress=0, r_spinner=True, r_stage='Getting Data to Restore for {}'.format(t_name), r_updaterunning=True)
            count = cursor.execute(counts[t]).fetchone()[0]
            d = cursor.execute(tc[t])
            try:
                session.query(t).delete()
            except:
                print('Failed to delete', sys.exc_info())
            lasttime = time()
            for i, r in enumerate(d):
                row = dict(zip(keys[t], r))
                if t is Song:
                    row['jingle'] = 0
                nr = t(**row)
                session.add(nr)
                session.commit()
                thistime = time()
                send_args[t_name+'_totaltracks'] = count
                send_args[t_name+'_checkedtracks'] = i+1
                if int(lasttime) != int(thistime):
                    cp = '{0:.1f}'.format(i/count*100)
                    avetime = (thistime - tstart) / (i + 1)
                    send_args[t_name+'_avetime'] = '{:.5f}'.format(avetime)
                    eta = (avetime * (count - (i+1))) / 60
                    if eta > 1:
                        finish = '{} minutes'.format(round(eta))
                    else:
                        finish = '{} seconds'.format(round(eta * 60))
                    send_update(self.ws, r_stage='Restoring {}: Estimated Time to Finish {}'.format(t_name, finish), r_progress=cp,  r_spinner=False, r_active=True, **send_args)
                    lasttime = thistime
            send_update(self.ws, r_progress=100, r_spinner=False, r_active=False, r_stage='Restore Completed', **send_args)

        updatedone = int(time())
        send_update(self.ws, r_progress=100, checkedtracks=i+1, r_spinner=False, r_active=False, r_stage='Restore Completed in {:.1f} minutes'.format((updatedone - realstarttime)/60))

        db.close()
        conn.close()

        print('Update took', updatedone - realstarttime)
        return True

