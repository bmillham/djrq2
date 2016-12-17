#encoding: cinje

: from ..helpers.helpers import request_link, aa_link
: from ..helpers.funcs import format_decimal, format_size, format_percent, time_length, time_ago
: from .. import table_args, caption_args

: def topx ctx, limit=10
<div class='table-responsive'>
 <table #{table_args}>
  <caption #{caption_args}>Top ${limit} Artists</caption>
  <tr><th>#</th><th>Artist</th><th>Songs</th></tr>
  : for c, r in enumerate(ctx.queries.get_top_10(limit=limit))
   <tr>
    <td>${c+1}</td>
    : use aa_link r, 'artist', td=True
    <td>${format_decimal(r.artist_count)}</td>
   </tr>
  : end
  : if limit == 10
   <tr><th colspan=3><a href='/stats/?topartists=75'>See Top 75 Artists</a></th></tr>
  : end
 </table>
</div>
: end
