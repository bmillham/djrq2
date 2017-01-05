#encoding: cinje

: from ..helpers.helpers import request_link, aa_link
: from .. import table_args, caption_args

: def mostrequested ctx
<div class='table-responsive'>
 <table #{table_args}>
  <caption #{caption_args}>10 Most Requested</caption>
  <tr><th># Plays</th><th>Title</th><th>Artist</th><th>Album</th><th>Last Requested By</th></tr>
  : for song in ctx.queries.get_top_requested()
   <tr>
    <td>${len(song.played_requests)}</td>
     : use request_link ctx, song, td=True
     : use aa_link song.artist, 'artist', td=True
     : use aa_link song.album, 'album', td=True
    <td>
    : try
     ${song.played_requests[0].name} ${ctx.time_ago(song.played_requests[0].t_stamp)}</td>
    : except
     &nbsp;
    : end
   </tr>
  : end
 </table>
</div>
: end
