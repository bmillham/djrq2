class DJHostExtension:
    """ Parse the host name to find the DJ name, and save info that
        will be used in various places """
    first = True # Parse the host name before anything else is done
    needs = {'request'}
    provides = {'djhost'}

    def __init__(self, **args):
        pass

    def prepare(self, context):
        host, sep, host_domain = context.request.host.partition('.')
        context.fulldj = host
        if '-' in host: # So we can handle dj-name and name
            prefix, host = host.split('-')
        else:
            prefix = ''

        context.host_domain = host_domain
        context.djname = host
        context.djprefix = prefix
        context.djhost = sep.join((host, host_domain))
        context.websocket_admin = 'http://{}/pub?id={}-admin'.format(context.request.host.split(':')[0], context.fulldj.lower())
        context.websocket = 'http://{}/pub?id={}'.format(context.request.host.split(':')[0], context.fulldj.lower())
