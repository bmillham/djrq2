# encoding: cinje

: from cinje.std.html import link, div, span
: from urllib.parse import urlencode, quote_plus

: def letterscountsbar ctx, letterscountslist
    : try
    :   selected_letter = ctx.selected_letter
    : except AttributeError
    :   selected_letter = None
    : end

    <div class="col-sm-1 list-group">
     : for row in letterscountslist
        : if row.letter == ''
            : print("Skip Letter: |{}|".format(row.letter), dir(row.letter))
            : continue
        :end
        : l = quote_plus(row.letter)
        <a href="/${ctx.resource.__resource__}/?letter=${l}"
           tip='${row.count}'
           class='list-group-item #{"active" if selected_letter == row.letter else ""}'>
           ${row.letter} <span class='badge'>${row.count}</span>
        </a>
     : end
    </div>
: end
