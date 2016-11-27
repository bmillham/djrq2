# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def requeststemplate title, ctx, requestlist
    : using page title, ctx, lang="en"
        <div class='container'>
        <div class="row table-responsive">
         <div class="col-md-12">
        <table #{table_args}>
         <caption #{caption_args}>Requests</caption>
         <tr><th>Artist</th><th>Title</th><th>Album</th><th>Length</th><th>Last Played By</th></tr>

         </table>
         </div>
         </div>
         </div>
    : end
: end
