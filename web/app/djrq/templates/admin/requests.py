# encoding: cinje

: from ..template import page as _page
: from .. import table_class, table_style, caption_args
: from ..helpers.helpers import aa_link

: def requeststemplate page=_page, title=None, ctx=None, requestlist=[], view_status=None, requestinfo=None
    : using page title, ctx, lang="en"
        : table_class.append('sortable')
        <table class="#{' '.join(table_class)}" style="#{' '.join(table_style)}" id='request-table'>
         <caption #{caption_args}>${requestlist.count()} Requests
         : try
            (${ctx.time_length(int(requestinfo.request_length))})
         : except TypeError
          : pass
         : end
         &nbsp;
         <div class='btn-group'>
          <button type='button' class='btn btn-xs btn-primary dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>
           Requests To View: ${view_status}<span class='caret'></span>
          </button>
          <ul class='dropdown-menu'>
           : for rv in ('New/Pending', 'Ignored', 'New', 'Pending', 'Played')
            : if rv != view_status
             <li><a href='/admin/?view_status=${rv}'>${rv}</a></li>
            : end
           : end
          </ul>
         </div>
         </caption>
         <thead>
         <tr>
          <th>Status</th><th>Artist</th><th>Album</th>
          <th>Title</th><th>Length</th><th>Requested By</th>
          <th>Comment</th><th>Requested</th><th>Last Played</th>
         </tr>
         </thead>
         <tbody>
         : for i, r in enumerate(requestlist)
            : try
                : use requestrow ctx, r
            : except AttributeError
                # TODO: Ignore missing songs for now, but this should probably be an error!
                : print('Missing song', r.song_id)
                <td colspan=7>Came across a bad row in the requests list for song id ${r.song_id}</td></tr>
            : end
            : if i % 50
             : flush
            : end
         : end
         </tbody>
        </table>
    : end
: end

: def requestrow ctx, row
    <tr id='rr_${row.id}'>
        <td data-value='${row.status}'>
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
        <td>${ctx.format_time(row.song.time)}</td>
        <td>${row.name}</td>
        <td>${row.msg}</td>
        <td data-value='${row.t_stamp}'>${ctx.time_ago(row.t_stamp)}</td>
        : try
            <td data-value='${row.song.played[0].date_played}'>${row.song.played[0].played_by} ${ctx.time_ago(row.song.played[0].date_played)}</td>
        : except
            <td data-value=''>&nbsp;</td>
        : end
    </tr>
: end
