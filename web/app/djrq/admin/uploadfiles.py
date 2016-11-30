# encoding: utf-8

from ..templates.admin.uploadfiles import uploadfilestemplate
from collections import defaultdict
import json
import os

class UploadFiles:
    __dispatch__ = 'resource'
    __resource__ = 'uploadfiles'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries
        self.uploaddir = os.path.join('privatefilearea', context.djname)
        self.shareddir = os.path.join('privatefilearea', 'shared')
        self.sharetype = None
        if not os.path.exists(self.uploaddir):
            os.makedirs(self.uploaddir)
        if not os.path.exists(self.shareddir):
            os.makedirs(self.shareddir)

    def private(self, *arg, **args):
        sharetype = 'private'
        workingdir = self.uploaddir
        if self._ctx.request.method == 'GET':
            return self.get(sharetype, workingdir, *arg, **args)
        elif self._ctx.request.method == 'POST':
            return self.post(sharetype, workingdir, *arg, **args)
        elif self._ctx.request.method == 'DELETE':
            return self.delete(workingdir, *arg, **args)

    def shared(self, *arg, **args):
        sharetype = 'shared'
        workingdir = self.shareddir
        if self._ctx.request.method == 'GET':
            return self.get(sharetype, workingdir, *arg, **args)
        elif self._ctx.request.method == 'POST':
            return self.post(sharetype, workingdir, *arg, **args)
        elif self._ctx.request.method == 'DELETE':
            return self.delete(workingdir, *arg, **args)

    def get(self, sharetype, workingdir, *arg, **args):
        if 'list' in args:
            files = defaultdict(list)
            onlyfiles = [f for f in os.listdir(workingdir) if os.path.isfile(os.path.join(workingdir, f))]
            for f in onlyfiles:
                files['files'].append({'name': f,
                                      'size': os.path.getsize(os.path.join(workingdir, f)),
                                      'url': '/admin/uploadfiles/{}/?file={}'.format(sharetype, f),
                                      'deleteUrl': '/admin/uploadfiles/{}/?file={}'.format(sharetype, f),
                                      'deleteType': 'DELETE',})

            return json.dumps(files)
        if 'file' in args:
            return open(os.path.join(workingdir, args['file']), 'rb')

        return uploadfilestemplate("Upload Files [{}]".format(sharetype.capitalize()), sharetype,  self._ctx, [])

    def post(self, sharetype, workingdir, *arg, **args):
        r = defaultdict(list)
        for f in args['files']:
            fn = os.path.join(workingdir, f.filename)
            with open(fn, 'wb') as wfile:
                for l in f.file.readlines():
                    wfile.write(l)
            r['files'].append({'name': f.filename,
                      'size': os.path.getsize(fn),
                      'url': '/admin/uploadfiles/{}/?file={}'.format(sharetype, f.filename),
                      'deleteUrl': '/admin/uploadfiles/{}/?file={}'.format(sharetype, f.filename),
                      'deleteType': 'DELETE',
                      })
        return json.dumps(r)

    def delete(self, workingdir, *arg, **args):
        os.remove(os.path.join(workingdir, args['file']))
        return "{}"
