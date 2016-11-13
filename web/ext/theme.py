import os
import fnmatch
import operator

class ThemeExtension:
    """ Find available bootstrap themes """
    #first = True # Parse the host name before anything else is done
    #needs = {'request'}
    provides = {'themes'}

    def __init__(self, **args):
        themedir = os.path.join(os.path.dirname(__file__), '..', 'app', 'djrq', 'public', 'bootstrap', 'css')
        themes = {}
        for root, dirs, files in os.walk(themedir):
            for name in files:
                if fnmatch.fnmatch(name, 'theme-*'):
                    tname = name.split('-')[1]
                    themes[tname.capitalize()] = os.path.join('/public', 'bootstrap', 'css', name)
        #self.themes = sorted(themes.items(), key=operator.itemgetter(0))
        #print(self.themes)
        self.themes = themes


    def prepare(self, context):
        context.__dict__['themes'] = self.themes
