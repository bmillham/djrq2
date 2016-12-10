# encoding: utf-8

import os
import json
from glob import glob
import zipfile
from time import sleep, time
from datetime import datetime
from ..templates.admin.updatedatabase import selectfile, selectdatabasefile, updatecomplete, updateprogress
from concurrent.futures import ThreadPoolExecutor
from .backupdatabase import backupdatabase

# To push status to database updates.
import requests

ctx = None

class UpdateDatabase:
    __dispatch__ = 'resource'
    __resource__ = 'updatedatabase'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        ctx = context
        self.uploaddir = os.path.join('privatefilearea', context.djname)
        self.ws = 'http://{}/pub?id={}-admin'.format(self._ctx.djhost.split(':')[0], self._ctx.djname.lower())

    def get(self, *arg, **args):
        files = []

        for pattern in ('[Gg][Zz]', '[Gg][Zz][Ii][Pp]', '[Zz][Ii][Pp]', '[Rr][Aa][Rr]'):
            files += glob(os.path.join(self.uploaddir, '*.' + pattern))
        return selectfile("Select Database File", self._ctx, files)

    def unpack(self, *arg, **args):
        ftype = args['fileselection'].split('.')[-1]
        fn = os.path.join(self.uploaddir, args['fileselection'])
        with zipfile.ZipFile(fn) as zf:
            for i in zf.infolist():
                zf.extract(i, self.uploaddir)

        files = []
        for pattern in ('dat', 'idx', '[Xx][Mm][Ll]'):
            files += glob(os.path.join(self.uploaddir, '*.' + pattern))
        return selectdatabasefile('Select Database File', self._ctx, files)

    def updatedatabase(self, *arg, **args):
        #backupdatabase(self)
        #self._startupdate()
        self._ctx.queries.is_updating(status=True)
        self.executor = ThreadPoolExecutor(max_workers=1)
        future = self.executor.submit(backupdatabase, self)
        future.add_done_callback(self._backupcomplete)
        #return {'html': 'Update running'}
        print('Update is running!')
        return updateprogress('Updating Database', self._ctx)

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
        from ..model.prokyon.song import Song
        from ..model.prokyon.played import Played
        from ..model.prokyon.mistags import Mistags
        from ..model.prokyon.requestlist import RequestList
        from ..model.nullsoft.nullsoftdb import MediaLibrary

        def send_update(ws, cp, rc, field=None, filename=None, updatedcount=None, newtrack=False):
            d = {'progress': cp,
                 'updateartist': rc['artist'],
                 'updatealbum': rc['album'],
                 'updatetitle': rc['title'],
                 'currentfile': rc['filename'],
                 'difference': None,
                }
            if field is not None:
                d['difference'] = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(rc['filename'], field, s[fieldmap[field]], rc[field])
                d['updatedcount'] = updatedcount
            if newtrack:
                d['newtrack'] = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(rc['filename'], rc['artist'], rc['album'], rc['title'])
            requests.post(ws, data=json.dumps(d))

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

        d = {'progress': 0,
             'stage': 'Starting Database Update',
            }
        requests.post(self.ws, data=json.dumps(d))
        winampdb = MediaLibrary(self.uploaddir, verbose=False)
        print("%d records in the winamp database" % winampdb.totalrecords)
        count = winampdb.totalrecords

        print("Building list of Auto Added tracks")
        d = {'progress': 0,
             'stage': 'Updating Database',
            }
        requests.post(self.ws, data=json.dumps(d))
        aa = self._ctx.db.query(Song).filter(Song.path == 'AutoAdded', Song.filename=='AutoAdded')
        autoadded = []
        for arow in aa:
            autoadded.append(arow)
        print("Found {} Auto Added tracks".format(len(autoadded)))

        d = {'progress': 0,
             'stage': 'Updating Database',
            }
        lartist = None
        lalbum = None
        lp = None
        updatedcount = 0
        currentids = []

        for i, rc in enumerate(winampdb.fetchall()):
            up, uf = ntpath.split(rc['filename'])

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
            if 'artist' in rc.keys():
                if rc['artist'] is None or rc['artist'] == '':
                    rc['artist'] = 'Unknown Artist'
            if 'album' in rc.keys():
                if rc['album'] is None or rc['album'] == '':
                    rc['album'] = 'Unknown Album'
            rc['path'] = up
            rc['filename'] = uf

            cp = float('{0:.1f}'.format(i/count*100))
            if lp != cp:
                send_update(self.ws, cp, rc)
                lp = cp
                la = rc['artist']

            try:
                s = self._ctx.db.query(Song).filter(Song.path==up, Song.filename==uf).one().__dict__
            except:
                new_track = {fieldmap[field]: rc[field] for field in fieldmap}
                new_track['_addition_time'] = datetime.utcnow()
                track = Song(**new_track)
                self._ctx.db.add(track)
                self._ctx.db.commit() # Must commit to get the id
                currentids += [track.id]
                send_update(self.ws, cp, rc, newtrack=True)
            else:
                diff = False
                to_update = {}
                for field in fieldmap:
                    if rc[field] != s[fieldmap[field]] and field != 'lastmodified':
                        send_update(self.ws, cp, rc, field=field, filename=uf, updatedcount=updatedcount+1)
                        lp = cp
                        diff = True
                        to_update[fieldmap[field]] = rc[field]
                if diff:
                    updatedcount += 1
                    print('Updated', self._ctx.db.query(Song).filter(Song.id==s['id']).update(to_update))
            currentids += [s['id']]
        drows = [x.id for x in self._ctx.db.query(Song.id).filter(~Song.id.in_(currentids)).distinct()]
        print('Deleted:', len(drows), drows)
        if len(drows) > 0:
            print('Getting played')
            playeddeleted = self._ctx.db.query(Played.track_id).filter(Played.track_id.in_(drows)).delete(synchronize_session=False)
            print('Deleted played:', playeddeleted)
            requestsdeleted = self._ctx.db.query(RequestList.song_id).filter(RequestList.song_id.in_(drows)).delete(synchronize_session=False)
            print('Requests deleted:', requestsdeleted)
            mistagsdeleted = self._ctx.db.query(Mistags.track_id).filter(Mistags.track_id.in_(drows)).delete(synchronize_session=False)
            print('Mistags deleted:', mistagsdeleted)
            songsdeleted = self._ctx.db.query(Song.id).filter(Song.id.in_(drows)).delete(synchronize_session=False)
            print('Songs deleted:', songsdeleted)
        print('Commiting')
        print('Commited', self._ctx.db.commit())