# encoding: cinje

: from .template import page
: from .letterscountsbar import letterscountsbar
: from .namelist import namelist

: def browsetemplate title, ctx, letterscountslist, names=None
    : using page title, ctx, lang="en"
        <div class="row">
        : if letterscountslist is not None
            : use letterscountsbar ctx, letterscountslist
        : end
        <div class="browselist">
        : if names is not None
            : flush
            : yield from namelist(ctx, names)
        : end
        </div>
        </div>
    : end
: end
