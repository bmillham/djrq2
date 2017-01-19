# encoding: cinje

: from .template import page
: from .helpers.helpers import request_link, aa_link
: from . import table_class, table_style, caption_args

: def _tracklist title, ctx, a, r, songs
    <div class='container'>
     <div class='table-responsive'>
     : table_class.append('sortable')
     <table class="#{' '.join(table_class)}" style="#{' '.join(table_style)}">
      <caption #{caption_args}>${title}</caption>
      <thead>
      <tr>
      : if r == 'Album'
       <th>Track #</th>
      : end
       <th data-defaultsign='AZ'>Title</th><th data-defaultsign='AZ'>Artist</th>
       <th data-defaultsign='AZ'>Album</th><th>Length</th><th>Last Played</th>
      </tr>
      <tbody>
      : for i, row in enumerate(songs)
       <tr>
        : if r == 'Album'
         <td>${row.track}</td>
        : end
        : use request_link ctx, row, td=True
        : use aa_link row.artist, 'artist', td=True
        : use aa_link row.album, 'album', td=True
        <td>${ctx.format_time(row.time)}</td>
        <td data-value='#{row.played[0].date_played if len(row.played) > 0 else ""}'>
         : if len(row.played) > 0
          ${ctx.time_ago(row.played[0].date_played)} by ${row.played[0].played_by}
          : if len(row.played) > 1
           &nbsp;<span class="badge pull-right" title="Played ${len(row.played)} times" data-html='1' data-toggle='popover' data-placement='left auto' data-trigger='hover' data-content="
           : for p in row.played
            ${p.played_by} ${ctx.time_ago(p.date_played)}<br>
           : end
           ">${len(row.played)}</span>
          : end
         : else
          &nbsp;
         : end
         </td>
        </tr>
        : if not (i % 49) and i != 0
         </tbody>
        : flush
        <tbody>
        : end
       : end
      </tbody>
     </table>
     </div>
     </div>
: end

: def tracklist ctx, a, dataonly=False, phrase=None, new_only=False
    : if 'Query' in str(type(a))
        : print("Its a query")
        : c = a.count()
        : songs = a
        : if new_only
         : if c == 0
          : n = '__nonewtracks__'
         : else
          : n = a[0].artist.fullname
         : end
        : else
         : n = 'Search'
        : end
    : else
     : try
        : c = len(a.songs)
        : songs = a.songs
        : n = a.fullname
     : except AttributeError
        : n = a[0]
        : c = a[1].count()
        : songs = a[1]
     : end
    : end
    : try
        : r = ctx.resource.__resource__.capitalize()
    : except AttributeError
        : r = 'Search'
    : end
    : if phrase
        : title = "Found {} matches for {}".format(c, phrase)
    : else
        : title = "{} {} tracks {} {}: {}".format(ctx.format_decimal(c),
        :                                         'new' if new_only else '',
        :                                         'on' if r == 'Album' else 'for',
        :                                         r,
        :                                         'No New Tracks' if n == '__nonewtracks__' else n)
    : end
    : if dataonly
        : flush
        : yield from _tracklist(title, ctx, a, r, songs)
    : else
        : using page title, ctx, lang="en"
            : flush
            : if n == '__nonewtracks__'
             <center><h3>No new tracks.</h3></center>
            : else
             : yield from _tracklist(title, ctx, a, r, songs)
            : end
        : end
    : end
: end
