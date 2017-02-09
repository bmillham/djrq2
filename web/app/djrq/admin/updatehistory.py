# encoding: utf-8

import os
from glob import glob
from ..templates.admin.updatehistory import selectfile, updatehistorysummary, updatehistoryspace
import sqlite3

class UpdateHistory:
    __dispatch__ = 'resource'
    __resource__ = 'updatehistory'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        ctx = context
        self.uploaddir = os.path.join('privatefilearea', context.djname)

    def get(self, *arg, **args):
        files = glob(os.path.join(self.uploaddir, 'history-*.sqlite'))
        return selectfile("Select History File", self._ctx, files)

    def view(self, *arg, **args):
        print('View', arg, args)
        fn = os.path.join(self.uploaddir, args['fileselection'])
        sqdb = sqlite3.connect(fn)
        sqdb.row_factory = sqlite3.Row
        cursor = sqdb.cursor()
        summary = {}
        valid_fields = ('empty', 'dash', 'space')

        if 'details' in args:
            if args['details'] not in valid_fields:
                print('Bad details arg')
                return None
            x = cursor.execute('select count(id) as fcount, id from fixedtable where recordtype=:rtype group by id', {'rtype':args['details']})
            return updatehistoryspace('Update Details', self._ctx, x, cursor, args)

        for t in valid_fields:
            x = cursor.execute('select count(id) as tcount from fixedtable where recordtype=:rtype', {'rtype': t}).fetchone()
            summary[t] = x['tcount']
        return updatehistorysummary('Update Summary', self._ctx, summary, args['fileselection'])
