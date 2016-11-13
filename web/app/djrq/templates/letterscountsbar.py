# encoding: cinje

: from cinje.std.html import link, div, span
: from urllib.parse import urlencode, quote_plus

: def letterscountsbar ctx, letterscountslist
    : try
    :   selected_letter = ctx.selected_letter
    : except AttributeError
    :   selected_letter = None
    : end

    <div class="col-sm-1">
     <div class="sidebar-nav">
      <div class="sidebar-nav navbar navbar-default" role="navigation">
       <div class="navbar-collapse collapse sidebar-navbar-collapse">
        <ul class="navbar navbar-nav sidebar-nav">
         : for row in letterscountslist
            : if row.letter == ''
                : print("Skip Letter: |{}|".format(row.letter), dir(row.letter))
                : continue
            :end
         : l = quote_plus(row.letter)
         <li style="text-align: center; width: 90px;" #{"class='active'" if selected_letter == row.letter else ""}>
            <a href="/${ctx.resource.__resource__}/?letter=${l}" tip='${row.count}'>${row.letter}
                <span class='badge'>${row.count}</span>
            </a>
         </li>
         : end
        </ul>
       </div>
      </div>
     </div>
    </div>
: end
