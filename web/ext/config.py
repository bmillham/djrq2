import yaml

class ConfigurationExtension:
    """ Parse the host name to find the DJ name, and save info that
        will be used in various places """
    first = True # Parse the host name before anything else is done
    needs = {'request'}
    provides = {'config'}

    def __init__(self, file=None):
        assert file is not None
        print('Reading config file')
        with open(file) as f:
            config = yaml.safe_load(f)
        self._config = config

    def start(self, context):
        print('Putting config info in context')
        context.config = self._config
