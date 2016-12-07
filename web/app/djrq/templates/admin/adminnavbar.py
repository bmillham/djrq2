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
        <li #{" class='active'" if resource == None else ''}>
         <a href='/admin'>
          <span class='glyphicon glyphicon-cog'></span> ${ctx.djname}
          <span class='badge'>${format_decimal(ctx.requests_info.request_count)}</span>
         </a>
        </li>
        : try
         : if ctx.session.authenticated
          <li #{" class='active'" if resource == 'mistags' else ''}><a href="/admin/mistags">Mistags</a></li>
          <li #{" class='active'" if resource == 'suggestions' else ''}><a href="/admin/suggestions">Suggestions</a></li>
          <li #{" class='active'" if resource == 'showinfo' else ''}><a href='/admin/showinfo'>Show Info</a></li>
          <li #{" class='active'" if resource == 'requestoptions' else ''}><a href='/admin/requestoptions'>Request Options</a></li>
          : if ctx.databasetype == 'ampache'
            <li #{" class='active'" if resource == 'catalogoptions' else ''}><a href='/admin/catalogoptions'>Catalog Selection</a></li>
          : end
        <li class='dropdown'>
         <a href='#' class='dropdown-toggle navbar-brand' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'>Upload Files<span class='caret'></span></a>
         <ul class='dropdown-menu'>
          <li><a href='/admin/uploadfiles/private'>Your Private Area</a></li>
          <li><a href='/admin/uploadfiles/shared'>DJ Shared Area</a></li>
         </ul>
        </li>
        <li #{" class='active'" if resource == 'updatedatabase' else ""}><a class='dbupdate' href='/admin/updatedatabase'>Update Database</a></li>
       </ul>

       <ul class='nav navbar-nav navbar-right'>
        #<p class='navbar-text dbupdate' id='dbupdate' style='display: none;'>Update Progress</p>

         : end
        : except AttributeError
         : pass
        : end
        : if ctx.queries.is_updating()
         : print("Is updating")
         <li>Updating</li>
        : end
        <li><a href="/lastplayed"><span class='glyphicon glyphicon-home'></span></a></li>
        <li><a href='/admin/auth/?logout'><span class='glyphicon glyphicon-off'></span></a></li>
        : if ctx.listeners is not None
         <li><a href='#'><span class='glyphicon glyphicon-headphones'></span>&nbsp;
                        <span id='listeners'>${ctx.listeners.current}</span>/<span id='maxlisteners'>${ctx.listeners.max}</span></a>
         </li>
        : end
        </ul>
      </div>
     </div>
    </nav>
: end
