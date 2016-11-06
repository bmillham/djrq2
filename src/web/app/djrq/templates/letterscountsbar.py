# encoding: cinje

: from cinje.std.html import link, div, span
: from urllib.parse import urlencode, quote_plus

: def letterscountsbar ctx, letterscountslist
	: try
	:	selected_letter = ctx.selected_letter
	: except
	:	selected_letter = None
	: end
#    <div class="text-center btn-group">
#        <button type="button" class="btn btn-xs btn-block btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
#            Browsing By&nbsp;${ctx.resource.__resource__.capitalize()} <span class="caret"></span>
#        </button>
#        <ul class="dropdown-menu">
#            <li>
#            : if ctx.resource.__resource__ == 'artist'
#                <a href="/album">Browse by Album</a>
#            : else
#                <a href="/artist">Browse by Artist</a>
#            : end
#            </li>
#        </ul>
#   </div>
#   <div class="container-fluid">
#   <div class="row">
    <div class="col-sm-1">
     <div class="sidebar-nav">
      <div class="sidebar-nav navbar navbar-default" role="navigation">
       <div class="navbar-collapse collapse sidebar-navbar-collapse">
        <ul class="navbar navbar-nav sidebar-nav">
         #<ul class="nav nav-pills col-xs-12" >
         : for row in letterscountslist
            : if row.letter == ''
                : print("Skip Letter: |{}|".format(row.letter), dir(row.letter))
                : continue
            :end
         : try
            : l = quote_plus(row.letter)
         : except
            : l = row.letter
         : end
         #<li tip="${l}" role="presentation" style="text-align: center; width: 90px;">
         <li style="text-align: center; width: 90px;" #{"class='active'" if selected_letter == row.letter else ""}>
         #<a href="/${ctx.resource.__resource__}/?${urlencode({'letter': row.letter})}">
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
#   </div>
: end
