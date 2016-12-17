#encoding: cinje

: from ..helpers.helpers import request_link, aa_link
: from ..helpers.funcs import format_decimal, format_size, format_percent, time_length, time_ago
: from .. import table_args, caption_args

: def top10 ctx, title, query
 <div class='table-responsive'>
  <table #{table_args}>
  <caption #{caption_args}>${title}</caption>
   <tr><th>Plays</th><th>Title</th><th>Artist</th><th>Album</th><th>Last Played</th></tr>
   : for played in query
    <tr>
     <td>${played.played_count}</td>
     : use request_link ctx, played.Played.song, td=True
     : use aa_link played.Played.song.artist, 'artist', td=True
     : use aa_link played.Played.song.album, 'album', td=True
     <td>${time_ago(played.date_played)}</td>
    </tr>
   : end
  </table>
 </div>
: end
