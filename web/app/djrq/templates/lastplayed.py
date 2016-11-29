# encoding: cinje

: from .template import page
: from .helpers.helpers import request_link, aa_link
: from .helpers.funcs import format_time, time_ago
: from . import table_args, caption_args

: def lastplayedtemplate title, ctx, lplist
    : using page title, ctx, lang="en"
        <div class="row table-responsive">
         <div class="col-md-12">
        <table #{table_args}>
         <caption #{caption_args}>${ctx.lastplay_count} Last Played</caption>
         <tbody>
         <tr><th>Artist</th><th>Title</th><th>Album</th><th>Length</th><th>Last Played By</th></tr>
         : for i, r in enumerate(lplist)
            <tr>
             <td>
              : use aa_link r.Played.song.artist, 'artist'
             </td>
             <td>
              : use request_link ctx, r.Played.song
             </td>
             <td>
             : if r.played_count > 1
              <span data-html='1' data-toggle='popover' data-placement='right auto' data-trigger='hover' title="On ${r.played_count} albums" data-content="
                : for a in ctx.queries.get_multi_albums(r.Played.song.artist.fullname, r.Played.song.title)
                 ${a.album.fullname}<br />
                : end
                ">On ${r.played_count} albums</span>
             : else
                : use aa_link r.Played.song.album, 'album'
             : end
             </td>
             <td>
             : if r.played_count > 1
               ${format_time(r.avg_time, is_avg=True)}
             : else
                ${format_time(r.Played.song.time)}
             : end
             </td>
             : pc = len(r.Played.song.played)
             : playlist = r.Played.song.played
             <td>
                ${playlist[0].played_by}
                ${time_ago(playlist[0].date_played)}
             : if pc > 1
              <span class='badge pull-right' title="Played ${pc} times" data-html='1' data-toggle='popover' data-placement='left auto' data-trigger='hover' data-content="
               : for p in playlist
                ${p.played_by}
                ${time_ago(p.date_played)}<br/>
               : end
              ">
                ${pc}</span>
             : end
            </tr>
            : if not (i % 9) and i != 0
                </tbody>
                : flush
                <tbody>
            : end
         : end
         </table>
         </div>
         </div>
    : end
: end
