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
        if 'emptytagfix' in args:
            self.emptytagfix = True
        else:
            self.emptytagfix = False
        self._ctx.queries.is_updating(status=True)
        send_update(self.ws, spinner=True, stage='Preparing to backup database', updaterunning=True)

        #backupdatabase(self)
        #self._startupdate()

        self._ctx.queries.is_updating(status=True)
        self.executor = ThreadPoolExecutor(max_workers=1)
        future = self.executor.submit(backupdatabase, self)
        future.add_done_callback(self._backupcomplete)
        print('Update is running!')
        #return updateprogress('Updating Database', self._ctx)
        #return selectdatabasefile('Updating Database', self._ctx)

    def _backupcomplete(self, future):
        future = self.executor.submit(self._startupdate)
        future.add_done_callback(self._updatecomplete)
        return True

    def _updatecomplete(self, future):
        self._ctx.queries.is_updating(status=False)
        self.executor.shutdown(wait=False)
        return True

    def _startupdate(self):
        import ntpath # Used because the winamp files have windows type paths
        from ..model.prokyon.song import pSong
        from ..model.prokyon.played import pPlayed
        from ..model.prokyon.mistags import pMistags
        from ..model.prokyon.requestlist import pRequestList
        import re

        dashre = re.compile('\s+-\s+') # To remove spaces around - in fields

        send_update(self.ws, progress=0, stage='Starting Database Update', active=True, spinner=True)

        ftype = self.fileselection.split('.')[-1]

        if ftype.lower() == 'xml':
            from ..model.nullsoft.nullsoftxml import MediaLibrary
        else:
            from ..model.nullsoft.nullsoftdb import MediaLibrary

        fieldmap = { # Map of winamp -> mysql fields
                    'title': 'title',
                    'artist': 'artist_fullname',
                    'album': 'album_fullname',
                    'year': 'year',
                    'trackno': 'track',
                    'length': 'time',
                    'lastmodified': '_addition_time',
                    'filesize': 'size',
                    'bitrate': 'bit_rate',
                   }

        if ftype == 'xml':
            winampdb = MediaLibrary(db=os.path.join(self.uploaddir, self.fileselection))
        else:
            winampdb = MediaLibrary(self.uploaddir, verbose=False)

        send_update(self.ws, totaltracks=winampdb.totalrecords)
        count = winampdb.totalrecords

        send_update(self.ws, stage='Finding AutoAdded Tracks')
        aa = self._ctx.db.query(pSong).filter(pSong.path == 'AutoAdded', pSong.filename=='AutoAdded')
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

        starttime = time()
        avetime = 0.0
        avelist = deque([], maxlen=500)
        lasttime = starttime

        processed = 0
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
                    if not dadded:
                        dashtags.append(rc.copy())
                        dadded = True
                    if self.fixdash:
                        rc[f] = df

                # Fix or report empty fields (use the above corrected stripped field to catch field like '  ' also
                if sf is None or sf == '':
                    ef = 'Unknown {}'.format(f.capitalize())
                else:
                    ef = rc[f]
                if ef != rc[f]:
                    if not eadded:
                        badtags.append(rc.copy())
                        eadded = True
                    if self.emptytagfix:
                        rc[f] = ef

            if rc in badtags and not self.emptytagfix: # Skip bad rows
                continue

            try:
                s = self._ctx.db.query(pSong).filter(pSong.path==rc['path'], pSong.filename==rc['filename']).one().__dict__
            except:
                print('Got exception looking for {} {}'.format(rc['path'], rc['filename']))
                print(sys.exc_info()[0])
                new_track = {fieldmap[field]: rc[field] for field in fieldmap}
                new_track['_addition_time'] = datetime.utcnow()
                new_track['path'] = rc['path']
                new_track['filename'] = rc['filename']
                new_track['jingle'] = 0

                try:
                    track = pSong(**new_track)
                except:
                    print("Something went wrong trying to add", new_track)
                    print(sys.exc_info()[0])
                else:
                    self._ctx.db.add(track)
                    self._ctx.db.commit() # Must commit to get the id
                    rc['id'] = track.id
                    newcount += 1
            else:
                diff = False
                to_update = {}
                for field in fieldmap:
                    if field == 'lastmodified': continue
                    if rc[field] != s[fieldmap[field]]:
                        lp = cp
                        diff = True
                        to_update[fieldmap[field]] = rc[field]
                        diffs.append('DIFF {} was "{}" now "{}"'.format(field, s[fieldmap[field]], rc[field]))
                if diff:
                    updatedcount += 1
                    self._ctx.db.query(pSong).filter(pSong.id==s['id']).update(to_update)
                rc['id'] = s['id']
            currentids.append(rc['id'])
            thistime = time()
            if int(lasttime) != int(thistime):
                cp = '{0:.1f}'.format(i/count*100)
                eta = (avetime * (count - processed)) / 60
                if eta > 1:
                    finish = '{} minutes'.format(round(eta))
                else:
                    finish = '{} seconds'.format(round(eta * 60))
                send_update(self.ws, totaltracks=count, progress=cp, checkedtracks=i+1, newcount=newcount, updatedcount=updatedcount, avetime=avetime, stage='Updating Database: Estimated Time to Finish {}'.format(finish), spinner=False)
            timeint = thistime - lasttime
            lasttime = thistime

            avelist.append(timeint)
            avetime = mean(avelist)
            processed += 1

        print('Final commit')
        self._ctx.db.commit()
        print('Total currentids', len(currentids))
        send_update(self.ws, progress=0, checkedtracks=processed, newcount=newcount, updatedcount=updatedcount, stage='Updating Database: Checking for deleted tracks', spinner=True)
        drows = [x.id for x in self._ctx.db.query(Song.id).filter(~Song.id.in_(currentids))]
        send_update(self.ws, deletedtracks=len(drows))
        if len(drows) > 0:
            send_update(self.ws, stage='Updating Database: Deleting Played', cp=20)
            playeddeleted = self._ctx.db.query(pPlayed.track_id).filter(pPlayed.track_id.in_(drows)).delete(synchronize_session=False)
            send_update(self.ws, progress=40, deletedplayed=playeddeleted, stage='Updating Database: Deleting Requests')
            requestsdeleted = self._ctx.db.query(pRequestList.song_id).filter(pRequestList.song_id.in_(drows)).delete(synchronize_session=False)
            send_update(self.ws, progress=60, deletedrequests=requestsdeleted, stage='Updating Database: Deleting Mistags')
            mistagsdeleted = self._ctx.db.query(pMistags.track_id).filter(pMistags.track_id.in_(drows)).delete(synchronize_session=False)
            send_update(self.ws, progress=80, deletedmistags=mistagsdeleted, stage='Updating Database: Deleting Tracks')
            songsdeleted = self._ctx.db.query(pSong.id).filter(pSong.id.in_(drows)).delete(synchronize_session=False)
            send_update(self.ws, progress=100)

        send_update(self.ws, progress=0, stage='Updating Database: Finalizing Changes')
        self._ctx.db.commit()
        send_update(self.ws, progress=100, stage='Database Updated', active=False, spinner=False)
        print("Update complete")

        # Save update problems. TODO: use a sqlite database possibly???
        with open(os.path.join(self.uploaddir, 'badtags.txt'), mode='w') as badtagfile:
            for r in badtags:
                print(r, file=badtagfile)
        with open(os.path.join(self.uploaddir, 'dashtags.txt'), mode='w') as dashtagfile:
            for r in dashtags:
                print(r, file=dashtagfile)
        with open(os.path.join(self.uploaddir, 'spacetags.txt'), mode='w') as spacetagfile:
            for r in spacetags:
                print(r, file=spacetagfile)
        with open(os.path.join(self.uploaddir, 'diffs.txt'), mode='w') as diffsfile:
            for r in diffs:
                print(r, file=diffsfile)
        print('Bad tags', len(badtags))
        print('Dash tags', len(dashtags))
        print('Space tags', len(spacetags))
        print('Diffs', len(diffs))
