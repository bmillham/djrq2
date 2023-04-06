#!python
# -- coding: utf-8 --
# encoding: utf-8

# IRC import
from djirc.irc import IRC
# Helpers

from helpers.update_database import update_database
from helpers.find_info import find_info

import requests
import yaml
import argparse
from web.ext.locale import LocaleExtension
from time import sleep
from djlist import DJList
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
parser.add_argument('--irc-nick',
                    default='BerthaButt',
                    help='The IRC user')
parser.add_argument('-c', '--config-file',
                    default='../web/app/djrq/config.yaml',
                    help='The DJRQ2 config file to use for site information')
parser.add_argument('--ice-server',
                    #default='192.168.68.114',
                    default="eldrad.local",
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
parser.add_argument('--use-ssl',
                    action='store_true',
                    help='Use https instead of http for websockets')
parser.add_argument('-n', '--no-updates',
                    action="store_true",
                    help='Do not update IRC/Websockets. Used for testing.')
parser.add_argument('-m', '--ignore-djs', default='autodj',
                    help='Comma separated list of DJs to ignore')
parser.add_argument('--autodj-mount-point', default='autodj',
                    help='The AutoDJ mount point')
parser.add_argument('-p', '--listen-mount-points', default='listen',
                    help='Comma separated list of DJ mount points to watch')
parser.add_argument('--url-map', default='autodj=listen',
                    help='Comma separated list of listen urls to correct')

args = parser.parse_args()

with open(args.config_file) as f:
    config = yaml.safe_load(f)

iceuri = f"http://{args.ice_server}:{args.ice_port}/status-json.xsl"
errorlog = "errors.txt"
djlist = DJList(config, args.site, args.use_ssl)
le = LocaleExtension() # For now, default to english
djlist.close_db()
le.prepare(djlist.context)
djs = djlist.djs

iserv = IceServer(args=args)
try:
    iserv.get()
except:
    print('Unable to contact IceCast')

#iserv.relay_get()

if args.no_updates:
    print('Will not connect to the IRC server.')
    requests = None
else:
    pass

djirc = IRC(server=args.irc_server, port=args.irc_port, channel=args.irc_channel, nick=args.irc_nick, no_irc=args.no_updates)
djirc.connect()

#icestats = IceStats(iceuri)
requestcount = {}
for dj in djs:
    requestcount[dj] = 0

previous = {'server_description': None,
            'listenurl': None,
            'genre': None,
            'title': None,
            'server_name': None,
            'listeners': {'current': 0,
                          'max': 0}}
while True:
    if not args.no_updates:
        djirc.send(send_now=True) # Needed to 'ping' the irc server so connection is not lost

    active_source = iserv.now_playing()

    if active_source is None:
        print("no source")
        sleep(10)
        continue

    if 'title' not in active_source:
        print('No title!')
        sleep(10)
        continue

    if previous['server_name'] != active_source['server_name']:
        previous['server_name'] = active_source['server_name']
        previous['dj_db'] = active_source['server_name'].split('-')[-1].lower()
    #if active_source.previous.description != active_source.description:
    if previous['server_description'] != active_source['server_description']:
        new_show = active_source['server_description']
        previous['server_description'] = active_source['server_description']
    else:
        new_show = None
    if previous['listenurl'] != active_source['listenurl']:
        new_listenurl = active_source['listenurl']
        for r in args.url_map.split(','):
            f, t = r.split('=')
            new_listenurl = new_listenurl.replace(f'/{f}', f'/{t}')
        #new_listenurl = active_source['listenurl'].replace('/autodj', '/listen')
        #new_listenurl = new_listenurl.replace('/foobar', '/listen')
        previous['listenurl'] = active_source['listenurl']
    else:
        new_listenurl = None
    if previous['genre'] != active_source['genre']:
        previous['genre'] = active_source['genre']
    if previous['title'] != active_source['title']:
        previous['title'] = active_source['title']
        #print(f'New Title: {active_source["server_name"]}: {active_source["title"]}')
        played_dj_name = active_source["server_name"]
        for d in djs:
            if d.lower() in played_dj_name.lower():
                active_source['dj_db'] = d.lower()
                found_title_info = find_info(djs[d.lower()].context, active_source['title'])
        #as_dj = active_source.dj_db

        current_dj_info = None
        for d in djs:
            update_played_only = False
            if active_source['dj_db'] != d:
                if active_source['dj_db'] == 'autodj':
                    continue
                #update_played_only = True
                as_dj = d
            else:
                as_dj = d
            #update_info = update_irc_songs(ctx=djs[d].context,
            update_info = update_database(ctx=djs[d].context,
                                          djlist=djlist,
                                          as_dj=as_dj,
                                          info=active_source,
                                          found_info=found_title_info,
                                          no_updates=args.no_updates,
                                          update_played_only=update_played_only,
                                          played_dj_name=played_dj_name)
            if update_info is None:
                print(f"{d}: Found 0 matches")
            else:
                print(f"{d}: Found {len(update_info['songs'])} matches")
            if  active_source['dj_db'] == d:
                current_dj_info = update_info
        update_info = current_dj_info
        try:
            #if len(update_info['song_lengths']) > 0:
            #    #length = f" [{', '.join(update_info['song_lengths'])}]"
            #    length = f" [{update_info['song_length']}]"
            #else:
            #    length = None
            length = f"{update_info['song_length']}"
        except TypeError:
            length = None
        db_artist = set()
        db_title = set()
        db_album = set()
        if update_info is None:
            print('No update_info')
            sleep(5)
            continue
        if update_info is not None:
            if update_info['songs'] is None:
                print('No songs to update')
                sleep(5)
                continue
            for song in update_info['songs']:
                db_artist.add(song.artist.fullname)
                db_title.add(song.title)
                db_album.add(song.album.fullname)
        if len(db_album) > 1:
            db_album = [f"On {len(db_album)} albums"]
        send_title = f"{active_source['server_name']}"
        if update_info is None:
            send_title += f" Playing: {active_source['title']}"
        else:
            if len(db_artist) == 0 and len(db_title) == 0 and len(db_album) == 0:
                send_title += f" Playing: {active_source['title']}"
            else:
                send_title += f" Playing: {'/'.join(db_artist)}"
                send_title += f" - {'/'.join(db_title)} - {'/'.join(db_album)}"
                if length is not None:
                    send_title += f" [{length}]"
        if new_show is not None:
            djirc.send(f"New DJ: {active_source['server_name']}", bold=True)
            djirc.send(f"New Show: {new_show}", bold=True)
        if new_listenurl is not None:
            djirc.send(f"Listen @ {new_listenurl}", bold=True)
        playing = [send_title]
        if update_info is not None:
            if update_info['requested_by'] is not None:
                    playing.append(f' (Requested by: {update_info["requested_by"]})')
        djirc.send(message=playing, bold=True, send_now=True)

    update_listen = False
    if previous['listeners']['max']  == -1:
        # Special case to trigger reading the database
        try:
            lrow = djs[active_source['dj_db']].db.Session.query(djs[active_source['dj_db']].context.listeners).one()
        except:
            print(f'Failed to get historical max listeners for {active_source["server_name"]}')
            previous['listeners']['max'] = 0
        else:
            print(f'Setting historical max listeners for {active_source["server_name"]} to {lrow.max}')
            previous['listeners']['max'] = lrow.max

    if previous['listeners']['current'] != active_source['listeners']:
        print(f"Change listeners to: {active_source['listeners']}")
        previous['listeners']['current'] = active_source['listeners']
        update_listen = True

    if active_source['listeners'] > previous['listeners']['max']:
        previous['listeners']['max'] = active_source['listeners']
        print(f'Change max listeners to: {previous["listeners"]["max"]}')
        update_listen = True

    if update_listen:
        lstr = [f"Listeners: {active_source['listeners']}/{previous['listeners']['max']},",
                f"DJ: {active_source['server_name']}"]
        djirc.send(message=lstr, send_now=True, action=True)
        ctx = djs[active_source['dj_db']].context
        try:
            lrow = djs[active_source['dj_db']].db.Session.query(ctx.listeners).one()
        except:
            print('No saved listener count')
        else:
            lrow.current = active_source['listeners']
            lrow.max = previous['listeners']['max']
            djs[active_source['dj_db']].db.Session.commit()
        l = {'listeners': active_source['listeners'],
             'maxlisteners': previous['listeners']['max']}
        if requests is not None:
            uri = djs[active_source['dj_db']].websocket
            requests.post(uri, json=l)
            requests.post(uri + '-admin', json=l)


    try:
        new_requests = djs[active_source['dj_db']].context.queries.get_requests_info(status='new')
    except Exception as e:
        print(f'Error running requests query for {active_source["dj_db"]} ({e})')
        try:
            djs[active_source.dj_db].db.Session.rollback()
        except Exception as rb_e:
            print(f'Unable to rollback because {rb_e}')
    else:
        if requestcount[active_source['dj_db']] != new_requests[0]:
            print(f'Updating requests: {new_requests[0]}')
            requestcount[active_source['dj_db']] = new_requests[0]
            if requests is not None:
                requests.post(djs[active_source['dj_db']].websocket, json={'requestbutton': new_requests[0]})

    sleep(1)
