#!/usr/bin/python
# -- coding: utf-8 --
# encoding: utf-8

# IRC imports
import irc.client
import irc.events

# pip3 install dbus-python
try:
    import dbus
except ModuleNotFoundError:
    print('Unable to import dbus, so will not attempt to restart autodj on failure')
    print('Install dbus with either apt install python3-dbus or pip3 install dbus-python')
    dbus = None
import requests
import cinje
import yaml
import sys
import argparse
from web.ext.locale import LocaleExtension
from web.app.djrq.templates.lastplayed import lastplayed_row
from sqlalchemy.ext.declarative import declarative_base
from time import sleep
from djlist import DJList
from icecast.iceserver import IceServer, IceDict

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
parser.add_argument('-p', '--mount-points', default='autodj,listen',
                    help='Comma separated list of mountpoint to watch')
parser.add_argument('-w', '--watchdog',
                    default=None,
                    help='Act as a watchdog for the named autodj service.')
parser.add_argument('--watchdog-only',
                    default=False,
                    action='store_true',
                    help='Only act as a watchdog for the autodj service. Do not update played or IRC.')

args = parser.parse_args()

joined = False
on_break = False

if dbus is not None:
    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
else:
    manager = None

# Setup IRC handlers
def on_connect(connection, event):
    print(f'IRC: {event.target} connected to {event.source}')
    for a in event.arguments:
        print(f'IRC: {a}')
    if irc.client.is_channel(args.irc_channel):
        connection.join(args.irc_channel)
        return
    print('IRC: Joined IRC without a target!')

def on_join(connection, event):
    global joined
    print(f"IRC: Joined {event.target}")
    joined = True

def update_irc_songs(ctx=None, as_dj=None, info=None, no_updates=None, update_played_only=False, fuzzy_match=False, played_dj_name=None):
    if played_dj_name is None:
        played_dj_name = info.dj
    try:
        dbsong = ctx.queries.get_song_by_ata(info.artist, info.song, info.album)
    except:
        print(f"Error querying the database for {info.title}!", file=sys.stderr)
    else:
        if dbsong.count() == 0:
            print(f"No full match was found for {ctx.db} {info.title}")
            try:
                dbsong = ctx.queries.get_song_by_artist_title(info.artist, info.song)
            except:
                print(f'Error searching for {info.title}')
                return
            if dbsong.count() == 0:
                print(f'Unable to find a match for {info.title}')

        for ds in dbsong:
            if not no_updates:
                try:
                    ctx.queries.add_played_song(track_id=ds.id, played_by=played_dj_name, played_by_me=True)
                except Exception as e:
                    print('Failed to update played into', e)
                    fakerow = None
                else:
                    try:
                        lpr = ctx.queries.get_last_played(count=1).one()
                    except:
                        print('Failed to get lpr')
                        fakerow = None
                    else:
                        fakerow = cinje.flatten(lastplayed_row(djlist.context,
                                                               lpr,
                                                               ma=False,
                                                               played=True,
                                                               show_played_time=False))
                if fakerow is not None and requests is not None:
                    lp = {'lastplay': fakerow}
                    uri = ctx.websocket
                    requests.post(uri, json=lp)
                else:
                    if requests is not None:
                        print('no fakerow')

        #if not update_played_only:
        #    ircclient.privmsg(args.irc_channel, f"\x02{info.dj} Playing: {info.title}\x0F")
        #    ircreactor.process_once()

if not args.watchdog_only:
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
        print('Unable to contact IRC')
    
    #iserv.relay_get()

if args.no_updates or args.watchdog_only:
    print('Will not connect to the IRC server.')
    ircclient = None
    requests = None
else:
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

#icestats = IceStats(iceuri)
requestcount = {}
for dj in djs:
    requestcount[dj] = 0

while True:
    if not args.no_updates:
        ircreactor.process_once()

    try:
        iserv.get() # Get latest data
    except:
        print('Problem reading icestats')
        if manager is not None and args.watchdog is not None:
            print(f'Restarting AutoDJ service: {args.watchdog}')
            try:
                job = manager.RestartUnit(f'{args.watchdog}.service', 'fail')
            except dbus.exceptions.DBusException as e:
                print(f'Failed to restart autodj {args.watchdog}: {e.get_dbus_message()}')
            sleep(30) # Give ezstream time to start before checking again
        continue
    
    try:
        active_source = iserv.icestats.sources.listen
    except AttributeError:
        active_source = iserv.icestats.sources.autodj

    if active_source.dj is None: # Must be listen with no active DJ
        try:
            active_source = iserv.icestats.sources.autodj
        except AttributeError:
            active_source = None
            print('No active source')
            sleep(10)
            continue

    if active_source.dj is None: # If still none, there must be no DJs!
        sleep(10)
        continue

    if 'title' not in active_source:
        print('No title!')
        sleep(10)
        continue

    if active_source.previous.description != active_source.description:
        print(f'New Show: {active_source.description}')
        new_show = active_source.description
        active_source.previous.description = active_source.description
    else:
        new_show = None
    if active_source.previous.listenurl != active_source.listenurl:
        print(f'New URL: {active_source.listenurl}')
        new_listenurl = active_source.listenurl.replace('/autodj', '/listen')
        active_source.previous.listenurl = active_source.listenurl
    else:
        new_listenurl = None
    if active_source.previous.genre != active_source.genre:
        print(f'New Genre: {active_source.genre}')
        active_source.previous.genre = active_source.genre
    if active_source.previous.title != active_source.title:
        active_source.previous.title = active_source.title
        print(f'New Title: {active_source.dj}: {active_source.title}')
        played_dj_name = active_source.dj
        as_dj = active_source.dj_db

        if ircclient is not None:
            if new_show is not None:
                ircclient.privmsg(args.irc_channel,
                              f"\x02New DJ: {active_source.dj}\x0F")
                ircclient.privmsg(args.irc_channel,
                                  f"\x02New Show: {new_show}\x0F")
            if new_listenurl is not None:
                ircclient.privmsg(args.irc_channel,
                                  f"\x02Listen @ {new_listenurl}\x0F")
            ircclient.privmsg(args.irc_channel,
                              f"\x02{active_source.dj} Playing: {active_source.title}\x0F")
            ircreactor.process_once()
        for d in djs:
            update_played_only = False
            if active_source.dj_db != d:
                if active_source.dj_db == 'autodj':
                    continue
                #update_played_only = True
                as_dj = d
            else:
                as_dj = d
            try:
                update_irc_songs(ctx=djs[d].context,
                                 as_dj=as_dj,
                                 info=active_source,
                                 no_updates=args.no_updates,
                                 update_played_only=update_played_only,
                                 played_dj_name=played_dj_name)
            except Exception as e:
                print(f'Failed to update irc and database: Try again in 10 seconds')
                print(e)
                #print('Aborting!')
                #exit(1)
                sleep(10)

    update_listen = False
    if active_source.previous.listeners.max == -1:
        # Special case to trigger reading the database
        try:
            lrow = djs[active_source.dj_db].db.Session.query(djs[active_source.dj_db].context.listeners).one()
        except:
            print(f'Failed to get historical max listeners for {active_source.dj}')
            active_source.previous.listeners.max = 0
        else:
            print(f'Setting historical max listeners for {active_source.dj} to {lrow.max}')
            active_source.previous.listeners.max = lrow.max

    if active_source.previous.listeners.current != active_source.listeners:
        print(f'Change listeners to: {active_source.listeners}')
        active_source.previous.listeners.current = active_source.listeners
        update_listen = True

    if active_source.listeners > active_source.previous.listeners.max:
        active_source.previous.listeners.max = active_source.listeners
        print(f'Change max listeners to: {active_source.previous.listeners.max}')
        update_listen = True

    if update_listen:
        lstr = (f"Listeners: {active_source.listeners}/{active_source.previous.listeners.max}, ",
                f"DJ: {active_source.dj}")
        if not args.no_updates:
            ircclient.action(args.irc_channel, ''.join(lstr))
        ctx = djs[active_source.dj_db].context
        try:
            lrow = djs[active_source.dj_db].db.Session.query(ctx.listeners).one()
        except:
            print('No saved listener count')
        else:
            lrow.current = active_source.listeners
            lrow.max = active_source.previous.listeners.max
            djs[active_source.dj_db].db.Session.commit()
        l = {'listeners': active_source.listeners,
             'maxlisteners': active_source.previous.listeners.max}
        if requests is not None:
            uri = djs[active_source.dj_db].websocket
            requests.post(uri, json=l)
            requests.post(uri + '-admin', json=l)


    try:
        new_requests = djs[active_source.dj_db].context.queries.get_requests_info(status='new')
    except Exception as e:
        print(f'Error running requests query for {active_source.dj_db} ({e})')
        try:
            djs[active_source.dj_db].db.Session.rollback()
        except Exception as rb_e:
            print(f'Unable to rollback because {rb_e}')
    else:
        if requestcount[active_source.dj_db] != new_requests[0]:
            print(f'Updating requests {new_requests}')
            requestcount[active_source.dj_db] = new_requests[0]
            if requests is not None:
                requests.post(djs[active_source.dj_db].websocket, json={'requestbutton': new_requests[0]})

    sleep(1)
