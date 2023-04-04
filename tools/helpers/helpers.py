""" Helpers """

from datetime import timedelta

class Helpers(object):
    def __init__(self):
        pass

    def sec_to_hms(self, seconds):
            s = str(timedelta(seconds=seconds)).split(':', 1)
            if int(s[0]) > 0:
                s[0] = f'{h:02}' # Force hour to be 2 digits
            else:
                s.pop(0) # Remove hour if 0
            return ':'.join(s)

    def find_info(self, ctx, title):
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
