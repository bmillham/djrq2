import requests
from time import time
#from .icemounts import IceMounts

class IceDict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError(f'No such attribute {name}')

    def __setattr__(self, name, value):
        self[name] = value


class IceServer(IceDict):
    def __init__(self, args=None):
        self._uri = f"http://{args.ice_server}:{args.ice_port}/status-json.xsl"
        if args.ice_relay is not None:
            self._relay_uri = f'http://{args.ice_relay}:{args.ice_relay_port}/status-json.xsl'
        else:
            self._relay_uri = None
        self._icestats = None
        self._last_check = None
        self._sources = {}
        self._listen_mount_points = args.listen_mount_points.split(',')
        self._autodj_mount_point = args.autodj_mount_point
        self._previous = IceDict({'title': None,
                                  'listeners': IceDict({'max': -1,
                                                        'current': -1})
        })
        self._listen = IceDict({})
        self._autodj = IceDict({})
        #self._mountpoints = IceMounts()

    def _get(self, relay=False, listen=False):
        if relay:
            uri = self._relay_uri
        else:
            uri = self._uri

        if uri is None:
            print('No IceCast to check.')
            return None
        #print('Getting icestats from', uri)
        try:
            self._icestats = IceDict(requests.get(uri).json()['icestats'])
        except:
            print(f'Problem getting stats from {uri}')
            raise IOError
        #print('got icestats', self._icestats)
        return self._icestats
        self._icestats.mountpoints = []

        if self._previous is None:
            self._previous = IceDict()

        self._icestats.sources = IceDict()
        if type(self._icestats.source) is dict:
            self._icestats.source = [self._icestats.source]
        for s in self._icestats.source:
            mp = s['listenurl'].split('/')[-1]
            if mp not in self._listen_mount_points[0]:
                continue
            self._icestats.mountpoints.append(mp)
            self._icestats.sources[mp] = IceDict(s)
            try:
                self._icestats.sources[mp].dj = s['server_name']
            except KeyError:
                self._icestats.sources[mp].dj = None

            if self._icestats.sources[mp].dj is None:
                self._icestats.sources[mp].dj_db = None
            else:
                self._icestats.sources[mp].dj_db = self._icestats.sources[mp].dj.split('-')[-1].lower()
            try:
                self._icestats.sources[mp].description = s['server_description']
            except KeyError:
                self._icestats.sources[mp].description = None
            try:
                self._icestats.sources[mp].listenurl = s['listenurl']
            except KeyError:
                self._icestats.sources[mp].listenurl = None
            try:
                self._icestats.sources[mp].genre = s['genre']
            except KeyError:
                self._icestats.sources[mp].genre = None
            #print(self._icestats.sources[mp])
            if mp not in self._previous or self._icestats.sources[mp].dj is None:
                #print(f'Creating previous for {mp}')
                self._previous[mp] = self._create_empty_mp()
                #print(self._previous[mp])
            mps = self._icestats.sources[mp]
            mps.mp = mp
            mps.previous = self._previous[mp]

            try:
                mps.artist, mps.song, mps.album = mps.title.split(' - ')
            except AttributeError:
                mps.artist = None
                mps.song = None
                mps.album = None
            except ValueError:
                #print(f'Bad title: {mps.title}')
                try:
                    mps.artist, mps.song = mps.title.split(' - ')
                except ValueError:
                    mps.artist = None
                    mps.song = None
                    mps.album = None
                else:
                    mps.album = None
            else:
                mps.artist.strip()
                mps.song.strip()
                mps.album.strip()

    def _create_empty_mp(self):
        return  IceDict({'title': None,
                                    'description': None,
                                    'genre': None,
                                    'listenurl': None,
                                    'listeners': IceDict({'max': 0,
                                                                      'current': 0})
                                  })

    def _mps(self):
        mp = []
        for s in self.sources:
            self._sources[s['listenurl'].split('/')[-1]] = s

    def get(self):
        self._get(relay=False)

    def relay_get(self, listen):
        self._get(relay=True, listen=listen)

    def now_playing(self):
        for listen in [True, False]:
            if listen:
                mps = self._listen_mount_points
            else:
                mps = [self._autodj_mount_point]
            for relay in [False, True]:
                listen_info = self._get(relay=relay, listen=listen)
                #print('listen info', listen_info)
                if type(listen_info['source']) == dict:
                    ls = [listen_info['source']]
                else:
                    ls = listen_info['source']
                for source in ls:
                    #print('source', source, relay)
                    mp = source['listenurl'].split('/')[-1]
                    #print('mp', mp)
                    if mp in mps:
                        if 'title' in source:
                            source['active_source'] = mp
                            #print('found mp', mp)
                            source['dj_db'] = source['server_name'].split('-')[-1].lower()
                            return source
        return None

    @property
    def icestats(self):
        if self._icestats is None:
            self.get()
        return self._icestats

    #@property
    #def previous(self):
    #    return self._previous

    #@property
    #def listeners(self):
    #    return None

    #@property
    #def admin(self):
    #    return self._icestats['admin']

    #@property
    #def host(self):
    #    return self._icestats['host']

    #@property
    #def location(self):
    #    return self._icestats['location']

    #@property
    #def server_id(self):
    #    return self._icestats['server_id']

    #@property
    #def server_start(self):
    #    return self._icestats['server_start']

    #@property
    #def sources(self):
    #    return self._icestats['source']

    @property
    def mountpoints(self):
        mp = []
        for s in self._icestats.source:
            mp.append(s['listenurl'].split('/')[-1])
        return mp

    #@property
    #def listeners(self, mp=None):
    #    l = {}
    #    if mp is not None:
    #        return self._sources[mp]['listeners']
    #    for m in self._sources:
    #        l[m] = self._sources[m]['listeners']
    #    return l
        
