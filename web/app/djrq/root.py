# encoding: utf-8

import importlib
from webob.exc import HTTPFound, HTTPError, HTTPNotFound
from web.app.static import static
from .templates.notfound import notfound
from .templates.tracklist import tracklist
from .model.lastplay import DJs
from .model.common import Listeners
import os

class Root:
    __dispatch__ = 'resource'

    # Import the album, artist, stats, requests and lastplayed endpoints.
    from .album import Album as album, Album
    from .artist import Artist as artist, Artist
    from .stats import Stats as stats, Stats
    from .requests import Requests as requests, Requests
    from .lastplayed import LastPlayed as lastplayed
    from .whatsnew import WhatsNew as whatsnew
    from .siteoptions import SiteOptions as siteoptions
    from .admin.admin import Admin as admin

    public = static(os.path.join(os.path.dirname(__file__), 'public'))

    def __init__(self, context=None, collection=None, record=None):
        """ Setup basic stuff needed for all pages """
        self._ctx = context

    def get(self, *arg, **args):
        """ Handle other endpoints not imported """
        if len(arg) == 0:
            return HTTPFound(location="/lastplayed") # Make lastplayed the default
        else:
            return notfound(self._ctx, arg[0])

    def post(self, content, *arg, **args):
        print("Got a post", content, arg, args )
        if content == 'search':
            if 'stext' not in args:
                l = self._ctx.queries.advanced_search(search_for=args['advsearchtype'].lower(), phrase=args['advsearchtext'])
                tl = tracklist(self._ctx, l, dataonly=True, phrase='{advsearchtype}: {advsearchtext}'.format(**args))
                r = ""
                for i in tl:
                    r += i
                return {'html' : r}
                #return tracklist(self._ctx, l)
                #return {'html': 'Search for {advsearchtype} {advsearchtext}'.format(**args)}
            else:
                l = self._ctx.queries.full_text_search(phrase=args['stext'])
                return tracklist(self._ctx, l, phrase=args['stext'])
        return notfound(self._ctx, content)
