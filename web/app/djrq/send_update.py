import requests

def send_update(ws, **args):
    """ Send websocket updates """

    if 'avetime' in args:
        args['avetime'] = f'{args["avetime"]:.5f}'
    print('sending update', ws)
    requests.post(ws, json=args)
