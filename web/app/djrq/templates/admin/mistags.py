# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def mistagstemplate title, ctx, requestlist
    : using page title, ctx, lang="en"
        <div class="row table-responsive">
         <div class="col-md-12">
        <table #{table_args}>
         <caption #{caption_args}>Mistags</caption>
         </table>
         </div>
         </div>
    : end
: end
