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
        fixdir = os.path.join(os.path.dirname(__file__), '..', 'app', 'djrq', 'public', 'themefixes')
        themes = {}
        fixes = {}
        for root, dirs, files in os.walk(themedir):
            for name in files:
                if fnmatch.fnmatch(name, 'theme-*'):
                    tname = name.split('-')[1]
                    themes[tname.capitalize()] = os.path.join('/public', 'bootstrap', 'css', name)
                    fixes[tname.capitalize()] = os.path.join('/public', 'themefixes', "fix-{}.css".format(tname))

        self.themes = themes
        self.fixes = fixes
        self.default_theme = args['default']

    def prepare(self, context):
        session = context.session
        try:
            csu = session.usertheme
        except AttributeError:
             csu = None

        if csu is None:
             theme = self.default_theme
        else:
            theme = csu

        context.__dict__['usertheme'] = theme
        context.__dict__['themes'] = self.themes
        context.__dict__['default_theme'] = self.default_theme

    def after(self, context):
        context.__dict__['fixes'] = self.fixes[context.usertheme]

