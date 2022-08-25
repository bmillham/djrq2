import requests
from time import time
#from .icemounts import IceMounts

class IceServer:
    def __init__(self, args=None):
        self._uri = f"http://{args.ice_server}:{args.ice_port}/status-json.xsl"
        if args.ice_relay is not None:
            self._relay_uri = f'http://{args.ice_relay}:{args.ice_relay_port}/status-json.xsl'
        else:
            self._relay_uri = None
        self._icestats = None
        self._last_check = None
        #self._mountpoints = IceMounts()

    def _get(self, relay=False):
        if relay:
            uri = self._relay_uri
        else:
            uri = self._uri

        if uri is None:
            print('No IceCast to check.')
            return None

        try:
            self._icestats = requests.get(uri).json()['icestats']
        except:
            print(f'Problem getting stats from {uri}')
            raise IOError

    def get(self):
        self._get(relay=False)

    def relay_get(self):
        self._get(relay=True)

    @property
    def icestats(self):
        if self._icestats is None:
            self.get()
        return self._icestats

    @property
    def listeners(self):
        return None
