# encoding: cinje

: from . import table_args

: def li_active resource, link
    <li
    : if resource == link
     class="active"
    : end
    >
    : yield
    </li>
: end

: def mainnavbar ctx
    : try
        : resource = ctx.resource.__resource__
    : except AttributeError
        : resource = None
    : end
    <nav class='navbar navbar-default navbar-fixed-top'>
     <div class='container-fluid'>
      <div class='collapse navbar-collapse' id='collapse-1'>
       <ul class='nav navbar-nav'>
        <li class='dropdown ${"active" if resource == "lastplayed" else ""}'>
         <a href='/lastplayed' class='dropdown-toggle navbar-brand' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'>${ctx.djname} <span class='badge'>${ctx.format_decimal(ctx.dbstats.total_songs)}</span><span class='caret'></span></a>
         <ul class='dropdown-menu'>
          <li #{" class='active'" if resource == 'lastplayed' else ''}><a href='/lastplayed'>Last Played</a></li>
         : if ctx.alldjs.count() > 1
            <li role='separator' class='divider'></li>
            : for d in ctx.alldjs
                : if d.dj != ctx.djname
                    : if ctx.djprefix != ''
                        : dj = '-'.join((ctx.djprefix, d.dj))
                    : else
                        : dj = d.dj
                    : end
                    <li><a href='http://${dj.lower()}.${ctx.host_domain}'>${d.dj}</a></li>
                : end
            : end
         : end
         </ul>
        </li>
        <li class='dropdown
        : if resource in ('artist', 'album')
         active
        : end
        '>
        : if ctx.dbstats.total_songs > 0
            <a href='#' class='dropdown-toggle' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'><span class='glyphicon glyphicon-eye-open'></span><span class='caret'></span></a>
            <ul class='dropdown-menu'>
             <li
               : if resource == 'artist'
                   class='active'
               : end
             ><a href="/artist">By Artist</a></li>
             <li
               : if resource == 'album'
                   class='active'
               : end
             ><a href="/album">By Album</a></li>
            </ul>
           </li>
           : using li_active resource, 'requests'
              <a href='/requests'><span class="hidden-md hidden-lg hidden-xl hidden-xxl">R</span>
              <span class="hidden-xs hidden-sm">Requests</span> <span class='badge'><span id="requestbutton">${ctx.format_decimal(ctx.requests_info.request_count)}</span></span></a>
           : end
           : if ctx.new_counts.new_count > 0
              <li #{" class='active'" if resource == 'whatsnew' else ''}>
                 <a href='/whatsnew'><span class="hidden-md hidden-lg hidden-xl hidden-xxl">N</span>
                 <span class="hidden-xs hidden-sm">New</span> <span class='badge'>${ctx.format_decimal(ctx.new_counts.new_count)}</span></a>
              </li>
           : end
           <li #{" class='active'" if resource == 'stats' else ''}><a href="/stats">Stats</a></li>
        : end
        <li class="hidden-xs hidden-sm"><a href="#" data-toggle='modal' data-target='#suggestionModal'>Suggestion</a></li>
       </ul>
       : if ctx.dbstats.total_songs > 0
           <form class='navbar-form navbar-left hidden-xs' action='/search' method='post' role='search'>
            <div class='form-group'>
             <div class='input-group'>
              <span class='input-group-addon'>
               <li class='nav navbar-nav'>
                <a href='#' data-toggle="modal" data-target='#searchModal'><span class='glyphicon glyphicon-search'></span></a>
               </li>
              </span>
              <input type='hidden' class='form-comtrol' name='navbarsearch' placeholder='Search'>
              <input type='text' class='form-comtrol hidden-xs hidden-sm' data-target="#searchModal" name='stext' id='stext' placeholder='Search'>
             </div>
            </div>
           </form>
       : end
       <ul class='nav navbar-nav navbar-right hidden-xs hidden-sm'>
        <li name='usericon' style='${"display:none" if not ctx.session.sitenick else ""}'><a href="#"><span class='glyphicon glyphicon-user'></span></a></li>
        <li><a href="/lastplayed"><span class='glyphicon glyphicon-home' aria-hidden='true' aria-label='Home'></span></a></li>
        <li class='dropdown'>
         <a href='#' class='dropdown-toggle' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'>
          <span class='glyphicon glyphicon-cog'></span>
          <span class='caret'></span>
         </a>
         <ul class='dropdown-menu'>
          <li><a href="/admin">Admin</a></li>
          <li><a href='/siteoptions'>Site Options</a></li>
          <li><a href='https://github.com/bmillham/djrq2/issues' target='_blank' rel='noopener noreferrer'>Report A Bug/Enhancement</a></li>
         </ul>
        </li>
        : if ctx.listeners is not None
            <li><a href='#'><span class='glyphicon glyphicon-headphones'></span>&nbsp;
                            <span id='listeners'>${ctx.listeners.current}</span>/<span id='maxlisteners'>${ctx.listeners.max}</span></a>
            </li>

        : end
        <li name='infoicon'>
         <a href='#' data-toggle='modal' data-target='#infoModal'>
          <span class='glyphicon glyphicon-info-sign' aria-hidden='true'></span>
         </a>
        </li>
       </ul>
       <ul class='nav navbar-nav navbar-right hidden-md hidden-lg'>
        <li class='dropdown'>
         <a href="#" class='dropdown-toggle' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'>
          <span class='glyphicon glyphicon-option-vertical'></span>
         </a>
         <ul class='dropdown-menu'>
          <li><a href='/admin'>Admin</a></li>
          <li><a href='/siteoptions'>Site Options</a></li>
         </ul>
        </li>
       </ul>
      </div>
     </div>
    </nav>
: end
