# encoding: cinje

: from .. import table_args

: def li_active resource, link
    <li
    : if resource == link
     class="active"
    : end
    >
    : yield
    </li>
: end

: def adminnavbar ctx -> strip
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
         <a class='navbar-brand' href='/admin'>
          <span class='glyphicon glyphicon-cog' aria-hidden='true'></span>&nbsp;${ctx.djname}&nbsp;
          <span id='requestbutton' class='badge'>${ctx.format_decimal(ctx.requests_info.request_count)}</span>
         </a>
        </li>
        : try
         : if ctx.session.authenticated
          <li #{" class='active'" if resource == 'mistags' else ''}>
           <a href="/admin/mistags">Mistags&nbsp;<span id='mistagsbutton' class='badge'>${ctx.format_decimal(ctx.mistags_count)}</span></a>
          </li>
          <li #{" class='active'" if resource == 'suggestions' else ''}>
           <a href="/admin/suggestions">Suggestions&nbsp;<span id='suggestionsbutton' class='badge'>${ctx.format_decimal(ctx.suggestions_count)}</span></a>
          </li>
          <li class='dropdown #{" active" if resource in ("showinfo", "requestoptions", "catalogoptions", "showhistory", "changepw") else ""}'>
           <a href='#' class='dropdown-toggle' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'>
            <span class='glyphicon glyphicon-wrench' aria-hidden='true' aria-label='Site Options'></span><span class='caret'></span></a>
           <ul class='dropdown-menu'>
            <li #{" class='active'" if resource == 'showinfo' else ''}><a href='/admin/showinfo'>Show Info</a></li>
            <li #{" class='active'" if resource == 'requestoptions' else ''}><a href='/admin/requestoptions'>Request Options</a></li>
            : if ctx.databasetype == 'ampache'
             <li #{" class='active'" if resource == 'catalogoptions' else ''}><a href='/admin/catalogoptions'>Catalog Selection</a></li>
            : end
            <li #{" class='active'" if resource == 'showhistory' else ""}>
             <a href='/admin/showhistory'>View History&nbsp;<span class='badge'>${ctx.git_total_commits}</span></a>
            </li>
            <li #{" class='active'" if resource == 'changepw' else ""}><a href='/admin/changepw'>Change Password</a></li>
           </ul>
          </li>

          <li class='dropdown'>
           <a href='#' class='dropdown-toggle' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'><span class='glyphicon glyphicon-cloud-upload' aria-hidden='true' aria-label='Upload Files'></span><span class='caret'></span></a>
           <ul class='dropdown-menu'>
            <li><a href='/admin/uploadfiles/private'>Your Private Area</a></li>
            <li><a href='/admin/uploadfiles/shared'>DJ Shared Area</a></li>
           </ul>
          </li>
          : if ctx.databasetype != 'ampache'
           <li #{" class='active'" if resource == 'updatedatabase' else ""}><a class='dbupdate' href='/admin/updatedatabase'>Update Database</a></li>
          : end
         : end
        : except AttributeError
         : pass
        : end
       </ul>
       <ul class='nav navbar-nav navbar-right'>
        <li><a href="/lastplayed"><span class='glyphicon glyphicon-home' aria-hidden='true' aria-label='Home'></span></a></li>
        <li><a href='/admin/auth/?logout'><span class='glyphicon glyphicon-log-out' aria-hidden='true' aria-label='Logoff'></span></a></li>
        : if ctx.listeners is not None
         <li><a href='#'><span class='glyphicon glyphicon-headphones' aria-hidden='true' aria-label='Listeners'></span>&nbsp;
                        <span id='listeners'>${ctx.listeners.current}</span>/<span id='maxlisteners'>${ctx.listeners.max}</span></a>
         </li>
        : end
        </ul>
      </div>
     </div>
    </nav>
: end
