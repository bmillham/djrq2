# encoding: utf-8

from ..templates.admin.mistags import mistagstemplate
from web.ext.acl import when

class Mistags:
    __dispatch__ = 'resource'
    __resource__ = 'mistags'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries

    def get(self, *arg, **args):
        if 'delete' in args:
            self.queries.delete_mistag(args['delete'])

        mistaglist = self._ctx.queries.get_mistags()
        for r in mistaglist:
            if r.title == r.song.title and \
               r.artist == r.song.artist.fullname and \
               r.album == r.song.album.fullname:
                   self._ctx.db.delete(r)
            self._ctx.db.commit()
        return mistagstemplate("Mistags", self._ctx,  mistaglist)
