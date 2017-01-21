# encoding: utf-8

from ..templates.admin.showhistory import showhistorytemplate, showdetails
from web.ext.acl import when

class ShowHistory:
    __dispatch__ = 'resource'
    __resource__ = 'showhistory'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context

    def get(self, *arg, **args):
        if 'commit' in args:
            commit = self._ctx.repo.commit(args['commit'])
            return showdetails('Commit Details', self._ctx, commit)

        return showhistorytemplate("Show Site History", self._ctx, self._ctx.git_commits)
