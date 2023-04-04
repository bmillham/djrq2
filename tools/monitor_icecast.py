#!/usr/bin/python
# -- coding: utf-8 --
# encoding: utf-8

# IRC imports
from djirc.irc import IRC

# pip3 install dbus-python
import requests
import cinje
import yaml
import sys
import argparse
from web.ext.locale import LocaleExtension
from web.app.djrq.templates.lastplayed import lastplayed_row
from sqlalchemy.ext.declarative import declarative_base
from time import sleep
from datetime import timedelta
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

args = parser.parse_args()

joined = False
on_break = False

def sec_to_hms(seconds):
    s = str(timedelta(seconds=seconds)).split(':', 1)
    if int(s[0]) > 0:
        s[0] = f'{h:02}' # Force hour to be 2 digits
    else:
        s.pop(0) # Remove hour if 0
    return ':'.join(s)

def find_info(ctx, title):
    """ Try and find a song when there are more than 3 fields in title"""

    site_options = ctx.queries.get_siteoptions()
    md_fields = site_options.metadata_fields.split(' - ')

    if site_options.strict_metadata:
        found_fields = title.split(' - ')
        if len(found_fields) != len(md_fields):
            print(f'Strict Metadata set and fields to not match for {title}')
            return [None] * 3
        else:
            return found_fields
        
    song_title = title.split(' - ')
    num_fields = len(fields)
    found = {}
    for field in md_fields:
        print('Working on', field, song_title)
        val = []
        while len(song_title) > 0:
            val.append(song_title.pop(0))
            l = ' - '.join(val)
            if field == 'artist':
                a = ctx.queries.get_artist(l)
            elif field == 'title':
                a = ctx.queries.get_title(found['artist'].id, l)
            elif field == 'album':
                if type(found['artist']) == list:
                    for art in found['artist']:
                        a = ctx.queries.get_album(art.id, l)
                        if a.count() > 0:
                            break
                else:
                    a = ctx.queries.get_album(found['artist'].id, l)
            else:
                print(f'ERROR: Unknow field: {field}')
            if a.count() > 0:
                if a.count() > 1:
                    print('found more than one match for', field)
                    found[field] = a.all()
                else:
                    found[field] = a.one()
                break

    titles = set()
    if type(found['title']) == list:
        for title in found['title']:
            titles.add(title.title)
    else:
        titles.add(found['title'].title)
    albums = set()
    if type(found['album']) == list:
        for album in found['album']:
            albums.add(album.album.prename)
    else:
        albums.add(found['album'].album.prename)
    if len(titles) == 1:
        titles = titles.pop()
    if len(albums) == 1:
        albums = albums.pop()

    song = ctx.queries.get_song_by_ata(found['artist'].fullname,
                                       titles, albums)
    if song.count() == 0:
        print('Giving up!')
        return None, None, None
    else:
        s = song.one()
        print('Found song id', s.id)
    return found['artist'].fullname, titles, albums
        
def update_irc_songs(ctx=None, as_dj=None, info=None, found_info=None, no_updates=None, update_played_only=False, fuzzy_match=False, played_dj_name=None):
    requested_by = None
    song_lengths = []
    #print('trying to update', info['title'])
    if played_dj_name is None:
        played_dj_name = info.dj
    info_parts = []
    #if info is None:
    #    print(f'Unable to process: {info}')
    #    return None
    #else:
    #    artist, title, album = find_info(ctx, info['title'])
        #try:
        #   artist, title, album = info['title'].split(' - ')
        #except ValueError:
        #    
        #    artist, title = info['title'].split(' - ')
        #    album = ''
        #info_parts = info['title'].split(' - ')
        #print('got', info_parts)
    #dbsong = ctx.queries.get_song_by_ata(found_info['artist'], found_info['title'], found_info['album'])
    try:
        dbsong = ctx.queries.get_song_by_ata(found_info[0], found_info[1], found_info[2])
    except:
        #print(f"Error querying the database for {found_info}!", file=sys.stderr)
        try:
            dbsong = ctx.queries.get_song_by_artist_title(found_info[0], found_info[1])
        except:
            #print(f"Error querying the database for {found_info} (2 fields)")
            print(f"Query error {found_info}")
            return None # Unable to find a match 

    #if dbsong.count() == 0:
        #print(f"No full match was found for {found_info}")
        #try:
        #    dbsong = ctx.queries.get_song_by_artist_title(found_info[0], found_info[1])
        #except:
        #    print(f'Error searching for {info["title"]}')
        #    return None
        #if dbsong.count() == 0:
        #    print(f'Unable to find a match for {info["title"]}')
    #print(f'Found {dbsong.count()} matches')
    songs = []
    for ds in dbsong:
        songs.append(ds)
        song_lengths.append(sec_to_hms(ds.time))
        try:
            req = ctx.queries.get_requests(status="New/Pending/Playing", id=ds.id)
        except Exception as e:
            print(f'Failed to find requests: {e}')
        else:
            if req.count() > 0:
                try:
                    r = req.one()
                except Exception as e:
                    print(f'Something went wong getting requestor: {e}')
                else:
                    print('Requested by', r.name)
                    requested_by = r.name
                try:
                    ctx.queries.update_request_to_played(r.id)
                except Exception as e:
                    print(f'Unable to update request status: {e}')

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
    return {'requested_by': requested_by,
            'song_lengths': song_lengths,
            'songs': songs}

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
        new_listenurl = active_source['listenurl'].replace('/autodj', '/listen')
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
            tt = ("B-52's - Private Idaho - Dance This Mess Around - The Best Of",
                  "Orchestre G.M.I - Groupement mobil d'intervention - Africa - Analog Africa n° 19 : Senegal 70",
                  "The Byrds - Chimes of Freedom - The Byrds, Dylan, Bob - The Byrds - Greatest Hits")
            if d == "sartre1":
                print('Doing sartre')
                for test_title in tt:
                    sid = find_info(djs[d].context, test_title)
                    print(f'{test_title} ID {sid}')
                #s = djs[d].context.queries.get_song_by_id(id=173291)
                #a = djs[d].context.queries.get_artist('The Byrds')
                #print(a.count())
                #print(s.artist_fullname)

            update_played_only = False
            if active_source['dj_db'] != d:
                if active_source['dj_db'] == 'autodj':
                    continue
                #update_played_only = True
                as_dj = d
            else:
                as_dj = d
            update_info = update_irc_songs(ctx=djs[d].context,
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
            if len(update_info['song_lengths']) > 0:
                length = f" [{', '.join(update_info['song_lengths'])}]"
            else:
                length = None
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
                    send_title += f" [{', '.join(update_info['song_lengths'])}]"
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
