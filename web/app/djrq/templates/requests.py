# encoding: cinje

: from .template import page as _page
: from . import table_class, table_style, caption_args
: from .helpers.funcs import time_ago, format_time
: from .helpers.helpers import aa_link, request_link

: def requeststemplate page=_page, title=None, ctx=None, requestlist=[]
    : using page title, ctx, lang="en"
      <div class='container'>
       <div class='table-responsive'>
        : table_class.append('sortable')
        <table class="#{' '.join(table_class)}" style="#{' '.join(table_style)}" id='request-table'>
         <caption #{caption_args}>Current Requests</caption>
         <thead>
         <tr>
          <th data-defaultsign='AZ'>Artist</th><th data-defaultsign='AZ'>Album</th>
          <th data-defaultsign='AZ'>Title</th><th>Length</th><th data-defaultsign='AZ'>Requestor</th>
          <th data-defaultsign='AZ'>Status</th><th data-defaultsign='month'>Last Requested</th>
         </tr>
         </thead>
         <tbody>
         : for r in requestlist
            : use requestrow ctx, r
         : end
         </tbody>
        </table>
       </div>
      </div>
    : end
: end

: def requestrow ctx, row
    <tr id='rr_${row.id}'>
        : use aa_link row.song.artist, 'artist', td=True
        : use aa_link row.song.album, 'album', td=True
        <td>
         : use request_link ctx, row.song, no_request_button=True
        </td>
        <td>${format_time(row.song.time)}</td>
        <td>${row.name}</td>
        <td>${row.status.capitalize()}</td>
        <td data-value='${row.t_stamp}'>${time_ago(row.t_stamp)}</td>
    </tr>
: end
