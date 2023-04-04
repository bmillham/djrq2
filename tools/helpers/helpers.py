""" Helpers """

from datetime import timedelta

class Helpers(object):
    def __init__(self):
        pass

    def sec_to_hms(self, seconds):
            s = str(timedelta(seconds=seconds)).split(':', 1)
            if int(s[0]) > 0:
                s[0] = f'{h:02}' # Force hour to be 2 digits
            else:
                s.pop(0) # Remove hour if 0
            return ':'.join(s)
