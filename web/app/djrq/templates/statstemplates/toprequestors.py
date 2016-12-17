#encoding: cinje

: from ..helpers.helpers import request_link, aa_link
: from ..helpers.funcs import format_decimal, format_size, format_percent, time_length, time_ago
: from .. import table_args, caption_args

: def toprequestors ctx
 <div class='table-responsive'>
  <table #{table_args}>
  <caption #{caption_args}>Top 10 Requestors</caption>
  <tr><th># Requests</th><th>Requestor</th><th>Last Request</th></tr>
  : for r in ctx.queries.get_top_requestors()
   <tr>
    <td>${r.request_count}</td>
    <td>${r.requestor}</td>
    <td>${time_ago(r.last_request)}</td>
   </tr>
  : end
 </table>
 </div>
: end
