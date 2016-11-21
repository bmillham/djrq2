import os
import fnmatch
import operator

class ThemeExtension:
    """ Find available bootstrap themes """
    #first = True # Parse the host name before anything else is done
    needs = {'session'}
    provides = {'themes'}

    def __init__(self, *arg, **args):
        themedir = os.path.join(os.path.dirname(__file__), '..', 'app', 'djrq', 'public', 'bootstrap', 'css')
        themes = {}
        padding = {}
        for root, dirs, files in os.walk(themedir):
            for name in files:
                if fnmatch.fnmatch(name, 'theme-*'):
                    tname, padd = name.split('-')[1:3]
                    themes[tname.capitalize()] = os.path.join('/public', 'bootstrap', 'css', name)
                    padding[tname.capitalize()] = padd

        self.themes = themes
        self.padding = padding
        self.default_theme = args['default']

    def prepare(self, context):
        session = context.session
        try:
            csu = session.usertheme
        except AttributeError:
            print("No session available")
            csu = None

        if csu is None:
            print("using default theme because session theme none:", self.default_theme)
            context.__dict__['usertheme'] = self.default_theme
        else:
            context.__dict__['usertheme'] = csu

        context.__dict__['themes'] = self.themes
        context.__dict__['padding'] = self.padding
        context.__dict__['default_theme'] = self.default_theme
