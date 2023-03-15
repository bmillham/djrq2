from .iceserver import IceServer

class IceMounts(IceServer):
    def __init__(self, stats=None):
        self._mountpoints = None

    def get(self):
        if self._stats is None:
            print('Get called with no stats')
            return None
        return self._stats
        
