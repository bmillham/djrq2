# encoding: cinje

: from .. import table_args
: from ..helpers.funcs import format_decimal

: def li_active resource, link
    <li
    : if resource == link
     class="active"
    : end
    >
    : yield
    </li>
: end

: def adminnavbar ctx
    : try
        : resource = ctx.resource.__resource__
    : except AttributeError
        : resource = None
    : end
    <nav class='navbar navbar-fixed-top navbar-inverse'>
     <div class='container-fluid'>
      <div class='collapse navbar-collapse' id='collapse-1'>
       <ul class='nav navbar-nav'>
        <li>
         <a href='/admin/requests'>
          <span class='glyphicon glyphicon-cog'></span> ${ctx.djname}
          <span class='badge'>${format_decimal(ctx.requests_info.request_count)}</span>
         </a>
        </li>
        : if ctx.session.authenticated
         <li><a href="/admin/mistags">Mistags</a></li>
         <li><a href="/admin/suggestions">Suggestions</a></li>
         <li><a href='/admin/showinfo'>Show Info</a></li>
         <li><a href='/admin/requestoptions'>Request Options</a></li>
         <li><a href='/admin/catalogoptions'>Catalog Selection</a></li>
        : end
       </ul>

       <ul class='nav navbar-nav navbar-right'>
        <li><a href="/lastplayed"><span class='glyphicon glyphicon-home'></span></a></li>
        <li><a href='/admin/auth/?logout'><span class='glyphicon glyphicon-off'></span></a></li>
        <li><a href='#'><span class='glyphicon glyphicon-headphones'></span>&nbsp;
                        <span id='listeners'>${ctx.listeners.current}</span>/<span id='maxlisteners'>${ctx.listeners.max}</span></a>
        </li>
        </ul>
      </div>
     </div>
    </nav>
: end
