# encoding: cinje

: from ..template import page as _page
: from .. import table_args, caption_args
: from ..helpers.funcs import time_ago, time_length, format_time
: from ..helpers.helpers import aa_link

: def requeststemplate page=_page, title=None, ctx=None, requestlist=[]
    : using page title, ctx, lang="en"
        <table id='request-table' #{table_args}>
         <caption #{caption_args}>${ctx.requests_info.request_count} Requests
         : try
            (${time_length(int(ctx.requests_info.request_length))})
         : except TypeError
          : pass
         : end
         </caption>
         <tr><th>Status</th><th>Artist</th><th>Album</th><th>Title</th><th>Length</th><th>Requested By</th><th>Last Requested</th></tr>
         : for r in requestlist
            : use requestrow r
         : end
        </table>
    : end
: end

: def requestrow row
    <tr id='rr_${row.id}'>
        <td>
            <div class="btn-group">
                <button type="button" class="btn btn-xs btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  ${row.status.capitalize()}<span class="caret"></span>
                </button>
                <ul class="dropdown-menu">
                : for status in ('Ignored', 'New', 'Pending', 'Played', 'Delete')
                 : if row.status.capitalize() != status
                    <li><a href=#{"/admin/?change_status&id={}&status={}".format(row.id, status.lower())}>${status.capitalize()}</a></li>
                 : end
                : end
                </ul>
            </div>
        </td>
        : use aa_link row.song.artist, 'artist', td=True
        : use aa_link row.song.album, 'album', td=True
        <td>${row.song.title}</td>
        <td>${format_time(row.song.time)}</td>
        <td>${row.name}</td>
        : try
            <td>${row.song.played[0].played_by} ${time_ago(row.song.played[0].date_played)}</td>
        : except
            <td>&nbsp;</td>
        : end
    </tr>
: end
