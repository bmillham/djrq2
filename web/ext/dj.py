from marrow.package.loader import load
from sqlalchemy.orm.exc import NoResultFound
from ..app.djrq.model.lastplay import DJs
from webob.exc import HTTPFound, HTTPError, HTTPNotFound

class DJExtension:
    needs = {'selective'}

    def __init__(self, config=None):
        self.whatsnewdays = config['whatsnew_days']
        self.lastplay_count = config['lastplay_count']

    def prepare(self, context):
        """ Setup basic stuff needed for all pages """

        context.__dict__['whatsnewdays'] = self.whatsnewdays
        context.__dict__['lastplay_count'] = self.lastplay_count
        try:
            djrow = context.db.lastplay.query(DJs).filter(DJs.dj == context.djname).one()
        except NoResultFound:
            raise HTTPNotFound('Host Not Found')

        context.__dict__['djname'] = djrow.dj

        package = 'web.app.djrq.model.'+djrow.databasetype

        context.__dict__['databasetype'] = djrow.databasetype
        context.__dict__['queries'] = load(package+'.queries:Queries')(db=context.db.default)
        Listeners = load(package + '.listeners:Listeners')

        try:
            album = load(package + '.album:Album', default='Album')
        except ImportError:
            album = 'Album'
        try:
            artist = load(package + '.artist:Artist', default='Artist')
        except ImportError:
            artist = 'Artist'

        context.__dict__['artist'] = artist
        context.__dict__['album'] = album
        context.__dict__['requestlist'] = load(package + '.requestlist:RequestList')
        context.__dict__['mistags'] = load(package + '.mistags:Mistags')
        context.__dict__['suggestions'] = load(package + '.suggestions:Suggestions')
        if context.queries.db is None:
            raise HTTPError("Queries is None!")
        context.__dict__['dbstats'] = context.queries.get_song_stats()
        context.__dict__['requests_info'] = context.queries.get_new_pending_requests_info()
        context.__dict__['new_counts'] = context.queries.get_new_counts(days=context.whatsnewdays)

        try:
            context.__dict__['listeners'] = context.db.default.query(Listeners).one()
        except NoResultFound:
            context.__dict__['listeners'] = None
        context.__dict__['alldjs'] = context.db.lastplay.query(DJs).filter(DJs.hide_from_menu == 0).order_by(DJs.dj)

