import cinje
import requests
from web.app.djrq.templates.lastplayed import lastplayed_row
from helpers.sec_to_hms import sec_to_hms
from statistics import mean

def update_database(ctx=None, djlist=None, as_dj=None, info=None, found_info=None,
                    no_updates=None, update_played_only=False,
                    fuzzy_match=False, played_dj_name=None):
    requested_by = None
    lengths = []
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
        lengths.append(ds.time)
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
    if len(lengths) == 1:
        song_length = sec_to_hms(lengths[0])
    else:
        song_length = f"~{sec_to_hms(mean(lengths))}"
    return {'requested_by': requested_by,
            'song_length': song_length,
            'songs': songs}

