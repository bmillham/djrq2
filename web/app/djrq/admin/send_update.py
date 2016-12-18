import requests
import json

def send_update(ws, **args):
    """ Send websocket updates """

    if 'avetime' in args:
        args['avetime'] = '{:.5f}'.format(args['avetime'])
    requests.post(ws, data=json.dumps(args))
