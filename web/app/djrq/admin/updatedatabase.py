# encoding: utf-8

import os
import json
from glob import glob
import zipfile
from time import sleep, time
from datetime import datetime
from ..templates.admin.updatedatabase import selectfile, updatedatabase, updatecomplete
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
        return updatedatabase('Update Database', self._ctx, files)

    def updatedatabase(self, *arg, **args):
        #backupdatabase(self)
        self._ctx.queries.is_updating(status=True)
        self.executor = ThreadPoolExecutor(max_workers=1)
        future = self.executor.submit(backupdatabase, self)
        future.add_done_callback(self._backupcomplete)
        return {'html': 'Update running'}

    def _backupcomplete(self, future):
        future = self.executor.submit(self._startupdate)
        future.add_done_callback(self._updatecomplete)
        return True

    def _updatecomplete(self, future):
        self._ctx.queries.is_updating(status=False)
        self.executor.shutdown(wait=False)
        return True

    def _startupdate(self):
        for i in range(100):
            d = {'progress': i+1}
            r = requests.post(self.ws, data=json.dumps(d))
            sleep(.25)
        return True
