#!/usr/bin/python

# IRC imports: pip install irc
try:
    import irc.client
    import irc.events
except ModuleNotFoundError:
    irc = None

import requests
import cinje
import yaml
import sys
import argparse
from marrow.package.loader import load
from web.ext.djdb import DJDatabaseExtension
from web.ext.locale import LocaleExtension
from web.app.djrq.model.lastplay import DJs
from web.app.djrq.templates.lastplayed import lastplayed_row
from sqlalchemy.ext.declarative import declarative_base
from time import sleep
from datetime import datetime
from djlist import DJList
from iceinfo import IceInfo, IceStats
from icecast.iceserver import IceServer

parser = argparse.ArgumentParser(description="Update an IRC channel and ampache database from an Icecast stream")
parser.add_argument('--irc-channel',
                    default='#rockit',
                    help='The IRC channel to join and announce on')
parser.add_argument('--irc-server',
                    default='eldrad.local',
                    help='The IRC server to connect to')
parser.add_argument('--irc-port',
                    default='6667',
                    help='The IRC port to use')
parser.add_argument('--irc-user',
                    default='BerthaButt',
                    help='The IRC user')
parser.add_argument('-c', '--config-file',
                    default='../web/app/djrq/config.yaml',
                    help='The DJRQ2 config file to use for site information')
parser.add_argument('--ice-server',
                    default='192.168.68.114',
                    help='The Icecast server to watch')
parser.add_argument('--ice-port',
                    default='8000',
                    help='The Icecast server port')
parser.add_argument('--ice-relay',
                    default=None,
                    help='Icecast relay server')
parser.add_argument('--ice-relay-port',
                    default='8000',
                    help='Icecast relay port')
parser.add_argument('--site',
                    default='rockitradio.local',
                    help='The DJRQ site to send updates to. Do not include the DJ in the site!')
parser.add_argument('-n', '--no-updates',
                    action="store_true",
                    help='Do not update IRC/Websockets. Used for testing.')


args = parser.parse_args()
Base = declarative_base()

joined = False
on_break = False

# Setup IRC handlers
def on_connect(connection, event):
    print(f'IRC: {event.target} connected to {event.source}')
    for a in event.arguments:
        print(f'IRC: {a}')
    if irc is None:
        return
    if irc.client.is_channel(args.irc_channel):
        connection.join(args.irc_channel)
        return
    print('IRC: Joined IRC without a target!')

def on_join(connection, event):
    global joined
    print(f"IRC: Joined {event.target}")
    joined = True

with open(args.config_file) as f:
    config = yaml.safe_load(f)

#iceuri = "http://192.168.1.2:8000/status-json.xsl"
iceuri = f"http://{args.ice_server}:{args.ice_port}/status-json.xsl"
errorlog = "errors.txt"
iceinfo = IceInfo(['autodj', 'listen'])
djlist = DJList(config, args.site)
le = LocaleExtension() # For now, default to english
djlist.close_db()
le.prepare(djlist.context)
djs = djlist.djs

#iserv = IceServer(args=args)
#iserv.get()
#print(iserv.icestats)
#if args.ice_relay is not None:
#    icerelay = f'http://{args.ice_relay}:{args.ice_relay_port}/status-json.xsl'
#    irelay = IceServer(uri=icerelay)
#    print(f'Connecting to ice_relay {icerelay}')
#    irelay.get()
#    print(irelay.icestats)

iserv = IceServer(args=args)
iserv.get()
print('iserv', iserv.icestats)
iserv.relay_get()
print('riserv', iserv.icestats)
#print('mp', iserv.mountpoints)

mountpoints = {}

if args.no_updates:
    print('Will not connect to the IRC server.')
elif irc is not None:
    print(irc)
    print(f'Connecting to IRC server: {args.irc_user}@{args.irc_server}/{args.irc_port}')
    ircreactor = irc.client.Reactor()
    try:
        ircclient = ircreactor.server().connect(args.irc_server, int(args.irc_port), args.irc_user)
    except irc.client.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    print(f'Connected. Joining {args.irc_channel}')

    ircclient.add_global_handler("welcome", on_connect)
    ircclient.add_global_handler("join", on_join)
    #c.add_global_handler("disconnect", on_disconnect)
    # Wait until the channel is joined
    print('Waiting to join')
    while not joined:
        ircreactor.process_once()
        sleep(.1)
    print('Joined')
    ircclient.action(args.irc_channel, f"Is on the job!")
    ircreactor.process_once()

icestats = IceStats(iceuri)

while True:
    if not args.no_updates and irc is not None:
        ircreactor.process_once()

    try:
        icestats.read_stats()
    except:
        print('Problem reading icestats')
        sleep(10)
        continue
    #print(f'l {icestats.listeners}, m {icestats.max_listeners}')
    for mount, data in icestats.mountpoints.items():
        if iceinfo.set_title(mount, data['title']):
            print('new title', mount, data['title'])
        try:
            art, song, alb = data['title'].split(' - ')
        except ValueError:
            print(f"Bad title on {mount}: {data['title']}", file=sys.stderr)
            continue
        except AttributeError: # When there is no title
            continue
        dj = data['dj'].lower().split('-')[-1]
        if 'otitle' not in data:
            data['otitle'] = None
        #print(f"got listeners {data['listeners']} o {data['olisteners']}")
        if 'olisteners' not in data:
            data['olisteners'] = 0
        if data['olisteners'] != data['listeners']:
            lstr = f"Listeners: {data['listeners']}/{data['max_l']}, DJ: {data['dj']}, MP: {mount}"
            print(lstr)
            if not args.no_updates and irc is not None:
                ircclient.action(args.irc_channel, lstr)
            ctx = djs[dj].context
            lrow = djs[dj].db.Session.query(ctx.listeners).one()
            lrow.current = data['listeners']
            if lrow.max < data['listeners']:
                lrow.max = data['listeners']
                data['max_l'] = data['listeners']
            else:
                data['max_l'] = lrow.max
            djs[dj].db.Session.commit()
            l = {'listeners': data['listeners'],
                 'maxlisteners': lrow.max}
            uri = djs[dj].websocket
            requests.post(uri, json=l)
            requests.post(uri + '-admin', json=l)
            data['olisteners'] = data['listeners']
        if on_break and not icestats.mountpoints['listen']['active']:
            on_break = False
            print("Back on duty")
            if not args.no_updates:
                ircclient.action(args.irc_channel, "finishes my last beer and gets back on duty.")
                ircreactor.process_once()
                ircclient.privmsg(args.irc_channel, f"\x02{mountpoints['autodj']['dj']} Playing: {mountpoints['autodj']['title']}\0f")
            
        if data['otitle'] != data['title']:
            print(f"{data['dj']}: {data['title']}")
            data['otitle'] = data['title']
            for d in djs:
                if djs[d].ignore_adj and dj == 'autodj':
                    #print(f'Ignore ADJ set for {d}, skipping update')
                    continue
                if icestats.mountpoints['listen']['active']:
                    if not on_break:
                        print("Switching to a live DJ")
                        if not args.no_updates:
                            ircclient.action(args.irc_channel, f"{data['dj']} is now streaming.")
                            ircreactor.process_once()
                        on_break = True
                    #print("Not updating ADJ because listen is active", icestats.mountpoints['listen'])
                    #continue
                else:
                    if on_break:
                        print("The live DJ left, back to AutoDJ")
                        if not args.no_updates:
                            ircclient.action(args.irc_channel, " AutoDJ is back on the job!")
                        on_break = False
                ctx = djs[d].context
                ctx.queries.catalogs = [1,3]
                try:
                    #dbsong = ctx.queries.get_song_by_ata('The Who', 'Behind Blue Eyes', "Who's Next")
                    dbsong = ctx.queries.get_song_by_ata(art.strip(), song.strip(), alb.strip())
                except:
                    print(f"{data['title']} was not found in the database!", file=sys.stderr)
                else:
                    for ds in dbsong:
                        if not args.no_updates:
                            ctx.queries.add_played_song(track_id=ds.id, played_by=data['dj'], played_by_me=True)
                        lpr = ctx.queries.get_last_played(count=1).one()
                        fakerow = cinje.flatten(lastplayed_row(djlist.context, lpr, ma=False, played=True, show_played_time=False))
                        lp = {'lastplay': fakerow}
                    if not args.no_updates:
                        requests.post(djs[d].websocket, json=lp)
                        if irc is not None:
                            ircclient.privmsg(args.irc_channel, f"\x02{data['dj']} Playing: {data['title']}\x0F")
                            ircreactor.process_once()

    sleep(1)

