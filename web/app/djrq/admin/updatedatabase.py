# encoding: utf-8

import os
from glob import glob
import zipfile
from rarfile import RarFile
from time import sleep, time
from datetime import datetime
from ..templates.admin.updatedatabase import selectfile, selectdatabasefile, updatecomplete, updateprogress
from concurrent.futures import ThreadPoolExecutor
from .backupdatabase import backupdatabase
from ..send_update import send_update
from collections import deque
from statistics import mean
import sys
import sqlite3

class UpdateDatabase:
    __dispatch__ = 'resource'
    __resource__ = 'updatedatabase'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        ctx = context
        self.uploaddir = os.path.join('privatefilearea', context.djname)
        self.ws = context.websocket_admin

    def get(self, *arg, **args):
        files = []

        if self._ctx.queries.is_updating():
            return selectdatabasefile('Updating Database', self._ctx)

        for pattern in ('[Gg][Zz]', '[Gg][Zz][Ii][Pp]', '[Zz][Ii][Pp]', '[Rr][Aa][Rr]'):
            files += glob(os.path.join(self.uploaddir, '*.' + pattern))
        return selectfile("Select Database File", self._ctx, files)

    def unpack(self, *arg, **args):
        ftype = args['fileselection'].split('.')[-1]
        fn = os.path.join(self.uploaddir, args['fileselection'])
        if ftype.lower() == 'rar':
            mod = RarFile
        elif ftype == 'zip':
            mod = zipfile.ZipFile

        with mod(fn) as zf:
            for i in zf.infolist():
                zf.extract(i, self.uploaddir)

        files = []
        for pattern in ('dat', 'idx', '[Xx][Mm][Ll]'):
            files += glob(os.path.join(self.uploaddir, '*.' + pattern))
        return selectdatabasefile('Select Database File', self._ctx, files)

    def updatedatabase(self, *arg, **args):
        self.fileselection = args['fileselection']
        if 'stripspaces' in args:
            self.stripspaces = True
        else:
            self.stripspaces = False

        self.fixdash = False

        if 'artisttagfix' in args:
            self.artisttagfix = True
        else:
            self.artisttagfix = False

        if 'albumtagfix' in args:
            self.albumtagfix = True
        else:
            self.albumtagfix = False

        if 'titletagfix' in args:
            self.titletagfix = True
        else:
            self.titletagfix = False

        send_update(self.ws, spinner=True, stage='Preparing to backup database', updaterunning=True)

        url = self._ctx.db[self._ctx.djname.lower()].session_factory.__dict__['kw']['bind'].url

        self._ctx.queries.is_updating(status=True)
        self.executor = ThreadPoolExecutor(max_workers=1)
        future = self.executor.submit(backupdatabase, self, url=url)
        future1 = self.executor.submit(self._startupdate, url=url)
        future1.add_done_callback(self._updatecomplete)
        print('Update is running!')

    def _backupcomplete(self, future):
        future = self.executor.submit(self._startupdate)
        future.add_done_callback(self._updatecomplete)
        return True

    def _updatecomplete(self, future):
        self._ctx.queries.is_updating(status=False)
        self.executor.shutdown(wait=False)
        return True

    def _startupdate(self, db=None, url=None):
        from sqlalchemy import create_engine
        from sqlalchemy.sql import select

        import ntpath # Used because the winamp files have windows type paths
        from ..model.prokyon.song import Song as pSong
        from ..model.prokyon.played import Played as pPlayed
        from ..model.prokyon.mistags import Mistags as pMistags
        from ..model.prokyon.requestlist import RequestList as pRequestList
        import re

        # Create a sqlite database to save update history info
        songtable = """CREATE TABLE tracks
                                        (rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                                         id INTEGER,
                                         title TEXT,
                                         artist TEXT,
                                         album TEXT,
                                         path TEXT,
                                         filename TEXT,
                                         recordtype TEXT)"""
        insrow = """INSERT INTO tracks
                                (id, title, artist, album, path, filename, recordtype)
                                VALUES
                                (:id, :title, :artist, :album, :path, :filename, :recordtype)"""
        fixedtable = """CREATE TABLE fixedtable (rowid INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER, field TEXT, val TEXT, oval TEXT, path TEXT, filename TEXT, recordtype TEXT)"""
        insfixed = """INSERT INTO fixedtable (id, field, val, oval, path, filename, recordtype) VALUES (:id, :field, :val, :oval, :path, :filename, :recordtype)"""
        statstable = """CREATE TABLE stats (
                                            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                                            totaltime FLOAT,
                                            avetime FLOAT,
                                            checked INTEGER,
                                            added INTEGER,
                                            updated INTEGER,
                                            deleted INTEGER,
                                            pdeleted INTEGER,
                                            rdeleted INTEGER,
                                            mdeleted INTEGER)"""
        insstats = "INSERT INTO stats (totaltime, avetime, checked, added, updated, deleted, pdeleted, rdeleted, mdeleted) VALUES (:totaltime, :avetime, :checked, :added, :updated, :deleted, :pdeleted, :rdeleted, :mdeleted)"
        sqdb = sqlite3.connect(os.path.join(self.uploaddir, 'history-{}.sqlite'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))))
        cursor = sqdb.cursor()
        try:
            cursor.execute(songtable)
        except:
            print('Failed to create table', sys.exc_info())
        try:
            cursor.execute(fixedtable)
        except:
            print('Failed to create fixedtable', sys.exc_info())
        try:
            cursor.execute(statstable)
        except:
            print('Failed to create stats', sys.exc_info())
        sqdb.commit()

        engine = create_engine(url)
        conn = engine.connect()

        dashre = re.compile('\s+-\s+') # To remove spaces around - in fields

        send_update(self.ws, progress=0, stage='Starting Database Update', active=True, spinner=True)

        ftype = self.fileselection.split('.')[-1]

        if ftype.lower() == 'xml':
            from ..model.nullsoft.nullsoftxml import MediaLibrary
        else:
            from ..model.nullsoft.nullsoftdb import MediaLibrary

        fieldmap = { # Map of winamp -> mysql fields
                    'title': 'title',
                    'artist': 'artist',
                    'album': 'album',
                    'year': 'year',
                    'trackno': 'tracknumber',
                    'length': 'length',
                    'lastmodified': 'lastModified',
                    'filesize': 'size',
                    'bitrate': 'bitrate',
                   }

        if ftype == 'xml':
            winampdb = MediaLibrary(db=os.path.join(self.uploaddir, self.fileselection))
        else:
            winampdb = MediaLibrary(self.uploaddir, verbose=False)

        send_update(self.ws, totaltracks=winampdb.totalrecords)
        count = winampdb.totalrecords

        send_update(self.ws, stage='Finding AutoAdded Tracks')

        aasel = select([pSong]).where(pSong.filename=='AutoAdded').where(pSong.path=='AutoAdded')
        aa = conn.execute(aasel)

        autoadded = []
        for arow in aa:
            autoadded.append(arow)
        print("Found {} Auto Added tracks".format(len(autoadded)))

        send_update(self.ws, stage='Updating Database')

        lartist = None
        lalbum = None
        lp = None
        updatedcount = 0
        currentids = []

        realstarttime = starttime = time()
        avetime = 0.0
        lasttime = starttime

        newcount = 0

        badtags = []
        dashtags = []
        spacetags = []
        diffs = []
        timestart = time()
        send_update(self.ws, totaltracks=count, spinner=False)

        for i, rc in enumerate(winampdb.fetchall()):
            rc['path'], rc['filename'] = ntpath.split(rc['filename'])

            if 'year' in rc.keys():
                rc['year'] = str(rc['year'])
            if 'filesize' in rc.keys():
                if rc['filesize'] is None:
                    rc['filesize'] = 0
                if rc['filesize'] < 1000000: rc['filesize'] *= 1000;
            if 'trackno' in rc.keys():
                if rc['trackno'] is None or rc['trackno'] == '':
                    rc['trackno'] = 0
            if 'bitrate' in rc.keys():
                if rc['bitrate'] is None or rc['bitrate'] == '':
                    rc['bitrate'] = 0

            fieldstofix = ('artist', 'album', 'title')

            sadded = False
            dadded = False
            eadded = False
            for f in fieldstofix:
                # Fix or report field with leading/trailing/extra spaces
                try:
                    sf = ' '.join(rc[f].split())
                except:
                    sf = rc[f]

                if sf != rc[f]:
                    try:
                        cursor.execute(insfixed, {'id':rc['id'], 'field':f, 'val':sf, 'oval':rc[f], 'path': rc['path'], 'filename': rc['filename'], 'recordtype':'space'})
                    except:
                        print('Error inserting', sys.exc_info())
                    sqdb.commit()
                    if not sadded:
                        spacetags.append(rc.copy())
                        sadded = True
                    if self.stripspaces:
                        rc[f] = sf

                # Fix or report fields with <space>-<space>
                try:
                    df = dashre.sub('-', rc[f])
                except:
                    df = rc[f]
                if df != rc[f]:
                    cursor.execute(insfixed, {'id':rc['id'], 'field':f, 'val':df, 'oval':rc[f], 'path': rc['path'], 'filename': rc['filename'], 'recordtype':'dash'})
                    if not dadded:
                        dashtags.append(rc.copy())
                        dadded = True
                    if self.fixdash:
                        rc[f] = df

                # Fix or report empty fields (use the above corrected stripped field to catch field like '  ' also
                if sf is None or sf == '' or rc[f] is None:
                    ef = 'Unknown {}'.format(f.capitalize())

                else:
                    ef = rc[f]
                if ef != rc[f]:
                    if not eadded:
                        badtags.append(rc)
                        eadded = True
                    if (self.artisttagfix and f == 'artist') or (self.albumtagfix and f == 'album') or (self.titletagfix and f == 'title'):
                        rc[f] = ef

            if rc in badtags:
                etagfound = False
                for f in fieldstofix:
                    if rc[f] == '' or rc[f] is None:
                        cursor.execute(insfixed, {'id':rc['id'], 'field':f, 'val':None, 'oval':None, 'path': rc['path'], 'filename': rc['filename'], 'recordtype':'empty'})
                        etagfound = True
                if etagfound:
                    #print('empty tags in', rc['artist'], rc['album'], rc['title'])
                    continue

            try:
                sel = select([pSong]).where(pSong.filename==rc['filename']).where(pSong.path==rc['path'])
            except:
                print('SQL failed', sys.exc_info())
            try:
                s = conn.execute(sel).fetchone()
            except:
                print('Execute failed', sys.exc_info())

            if s is None:
                new_track = {fieldmap[field]: rc[field] for field in fieldmap}
                new_track['lastModified'] = datetime.utcnow()
                new_track['path'] = rc['path']
                new_track['filename'] = rc['filename']
                new_track['jingle'] = 0

                try:
                    track = pSong.__table__.insert().values(**new_track)
                except:
                    print("Something went wrong trying to add", new_track)
                    print(sys.exc_info()[0])
                else:
                    res = conn.execute(track)
                    rc['id'] = res.inserted_primary_key[0]
                    newcount += 1
            else:
                diff = False
                to_update = {}
                for field in fieldmap:
                    if field == 'lastmodified': continue
                    if rc[field] != s[fieldmap[field]]:
                        diff = True
                        to_update[fieldmap[field]] = rc[field]
                        cursor.execute(insfixed, {'id':rc['id'], 'field':field, 'val':rc[field], 'oval': s[fieldmap[field]], 'path': rc['path'], 'filename': rc['filename'], 'recordtype':'updated'})
                        diffs.append('DIFF {} was "{}" now "{}"'.format(field, s[fieldmap[field]], rc[field]))
                if diff:
                    updatedcount += 1
                    try:
                        upd = pSong.__table__.update().where(pSong.id==s['id']).values(**to_update)
                    except:
                        print('Create failed', sys.exc_info())
                    try:
                        res = conn.execute(upd)
                    except:
                        print('Execute failed', sys.exc_info())
                rc['id'] = s['id']
            currentids.append(rc['id'])
            thistime = time()
            if int(lasttime) != int(thistime):
                cp = '{0:.1f}'.format(i/count*100)
                avetime = (thistime - realstarttime) / (i + 1)
                eta = (avetime * (count - (i+1))) / 60
                if eta > 1:
                    finish = '{} minutes'.format(round(eta))
                else:
                    finish = '{} seconds'.format(round(eta * 60))
                send_update(self.ws, totaltracks=count, progress=cp, checkedtracks=i+1, newcount=newcount, updatedcount=updatedcount, avetime=avetime, stage='Updating Database: Estimated Time to Finish {}'.format(finish), spinner=False)

            lasttime = thistime

        send_update(self.ws, progress=0, checkedtracks=i+1, newcount=newcount, updatedcount=updatedcount, stage='Updating Database: Checking for deleted tracks', spinner=True)
        del_sel = select([pSong.id]).where(~pSong.id.in_(currentids))
        drows = [x.id for x in conn.execute(del_sel)]
        send_update(self.ws, deletedtracks=len(drows))
        if len(drows) > 0:
            print('Deleted tracks', len(drows))
            send_update(self.ws, stage='Updating Database: Deleting Played', cp=20)
            playeddeleted = conn.execute(pPlayed.__table__.delete().where(pPlayed.track_id.in_(drows))).rowcount
            send_update(self.ws, progress=40, deletedplayed=playeddeleted, stage='Updating Database: Deleting Requests')
            requestsdeleted = conn.execute(pRequestList.__table__.delete().where(pRequestList.song_id.in_(drows))).rowcount
            send_update(self.ws, progress=60, deletedrequests=requestsdeleted, stage='Updating Database: Deleting Mistags')
            mistagsdeleted = conn.execute(pMistags.__table__.delete().where(pMistags.track_id.in_(drows))).rowcount
            send_update(self.ws, progress=80, deletedmistags=mistagsdeleted, stage='Updating Database: Deleting Tracks')
            songsdeleted = conn.execute(pSong.__table__.delete().where(pSong.id.in_(drows))).rowcount
            send_update(self.ws, progress=100)
        else:
            playeddeleted = requestsdeleted = mistagsdeleted = songsdeleted = 0

        send_update(self.ws, progress=100, stage='Database Updated', active=False, spinner=False)
        print("Update complete")

        totalupdatetime = time() - realstarttime
        print('Saving stats')
        istats = {'totaltime': totalupdatetime,
                                'avetime': avetime,
                                'checked': i+1,
                                'added': newcount,
                                'updated': updatedcount,
                                'deleted': songsdeleted,
                                'pdeleted': playeddeleted,
                                'rdeleted': requestsdeleted,
                                'mdeleted': mistagsdeleted}
        print('Printing stats')
        print('Saving update stats', istats)
        try:
            cursor.execute(insstats, istats)
        except:
            print('Failed to insert stats', sys.exc_info())

        sqdb.commit()
        conn.close()



        # Save update problems. TODO: use a sqlite database possibly???
        with open(os.path.join(self.uploaddir, 'badtags.txt'), mode='w') as badtagfile:
            for r in badtags:
                print(r, file=badtagfile)
                try:
                    cursor.execute(insrow, {**r, 'recordtype': 'empty'})
                except:
                    print('Failed to create table', sys.exc_info())
            sqdb.commit()
        with open(os.path.join(self.uploaddir, 'dashtags.txt'), mode='w') as dashtagfile:
            for r in dashtags:
                print(r, file=dashtagfile)
                cursor.execute(insrow, {**r, 'recordtype': 'dash'})
            sqdb.commit()
        with open(os.path.join(self.uploaddir, 'spacetags.txt'), mode='w') as spacetagfile:
            for r in spacetags:
                print(r, file=spacetagfile)
                cursor.execute(insrow, {**r, 'recordtype': 'space'})
            sqdb.commit()
        with open(os.path.join(self.uploaddir, 'diffs.txt'), mode='w') as diffsfile:
            for r in diffs:
                print(r, file=diffsfile)

        print('Bad tags', len(badtags))
        print('Dash tags', len(dashtags))
        print('Space tags', len(spacetags))
        print('Diffs', len(diffs))
        sqdb.close()
