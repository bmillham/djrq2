# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def authtemplate title, ctx, requestlist
    : using page title, ctx, lang="en"
        Authentication Page
    : end
: end
