# encoding: cinje

: from .template import page as _page
: from . import table_args, caption_args
: from .helpers.funcs import time_ago
: from .helpers.helpers import aa_link

: def requeststemplate page=_page, title=None, ctx=None, requestlist=[]
    : using page title, ctx, lang="en"
      <div class='container'>
       <div class='table-responsive'>
        <table #{table_args} id='request-table'>
         <caption #{caption_args}>Current Requests</caption>
         <tr><th>Artist</th><th>Album</th><th>Title</th><th>Requestor</th><th>Status</th><th>Last Requested</th></tr>
         : for r in requestlist
            : use requestrow r
         : end
        </table>
       </div>
      </div>
    : end
: end

: def requestrow row
    <tr>
        : use aa_link row.song.artist, 'artist', td=True
        : use aa_link row.song.album, 'album', td=True
        <td>${row.song.title}</td>
        <td>${row.name}</td>
        <td>${row.status.capitalize()}</td>
        <td>${time_ago(row.t_stamp)}</td>
    </tr>
: end
