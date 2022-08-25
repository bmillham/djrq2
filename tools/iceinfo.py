import requests

class IceMount:
    def __init__(self, mount):
        self._title = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title
    
class IceInfo:
    def __init__(self, mounts):
        self._mount = {}
        for m in mounts:
            self._mount[m] = IceMount(m)

    def set_title(self, mnt, new_title):
        if self._mount[mnt].title == new_title:
            return False
        else:
            self._mount[mnt].title = new_title
            return True

class IceSource:
    def __init__(self, source):
        pass

class IceStats:
    def __init__(self, iceserver):
        self._server = iceserver
        self._stats = None
        self._mountpoints = {}
        self._djs = {}

    def read_stats(self):
        #print(f'Getting stats from {self._server}')
        try:
            self._stats = requests.get(self._server).json()['icestats']
        except:
            print('Problem accessing:', self._server)
            raise IOError
        #print(f'full stats: {self._stats}')
        if 'source' not in self._stats:
            print('No sources found')
            raise KeyError
        if type(self._stats['source']) is dict:
            self._sources = [self._stats['source']]
        else:
            self._sources = self._stats['source']
        self._get_mountpoints()

    def _get_mountpoints(self):
        for source in self.sources:
            mp = source['listenurl'].split('/')[-1]
            if mp not in self._mountpoints:
                print(f"Found a new mountpoint {mp}")
                self._mountpoints[mp] = {'olisteners': -1,
                                         'otitle': None,
                                         'active': False,
                                         'listeners': 0,
                                         'max_l': 0,
                                         'dj': None,
                                         'show_name': None,
                                         'title': None}
            #print(f'source: {source}')
            if 'listeners' in source:
                self._mountpoints[mp]['listeners'] = source['listeners']
            if 'server_name' in source:
                self._mountpoints[mp]['dj'] = source['server_name']
            if 'server_description' in source:
                self._mountpoints[mp]['show_name'] = source['server_description']
            if 'title' in source:
                self._mountpoints[mp]['title'] = source['title']
            if 'stream_start' in source:
                self._mountpoints[mp]['active'] = True
        if 'listen' not in self._mountpoints:
            self._mountpoints['listen'] = {'active': False,
                                           'listeners': 0,
                                           'max_l': 0,
                                           'title': None}

    @property
    def sources(self):
        return self._sources

    @property
    def mountpoints(self):
        return self._mountpoints

    @property
    def listeners(self):
        return self._mountpoints['listen']['listeners']

    @property
    def max_listeners(self):
        return self._mountpoints['listen']['max_l']

