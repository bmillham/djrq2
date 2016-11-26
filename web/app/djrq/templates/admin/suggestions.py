# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def suggestionstemplate title, ctx, suggestionlist
    : using page title, ctx, lang="en"
        <div class="row table-responsive">
         <div class="col-md-12">
        <table #{table_args}>
         <caption #{caption_args}>Suggestions (${suggestionlist.count()})</caption>
         <tr>
          <th>Action</th><th>Artist</th><th>Album</th><th>Title</th><th>Suggested By</th><th>Comments</th>
         </tr>
         : for r in suggestionlist
          <tr>
           <td><a href='/admin/suggestions/?delete=${r.id}' class='btn btn-xs btn-primary'>Delete</a></td>
           <td>${r.artist}</td>
           <td>${r.album}</td>
           <td>${r.title}</td>
           <td>${r.suggestor}</td>
           <td>${r.comments}</td>
          </tr>
         : end
         </table>
         </div>
         </div>
    : end
: end
