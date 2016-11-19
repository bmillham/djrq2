# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def suggestionstemplate title, ctx, requestlist
    : using page title, ctx, lang="en"
        <div class="row table-responsive">
         <div class="col-md-12">
        <table #{table_args}>
         <caption #{caption_args}>Suggestions</caption>
         </table>
         </div>
         </div>
    : end
: end
