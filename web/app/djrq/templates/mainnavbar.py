# encoding: cinje

: from . import table_args
: from .helpers.funcs import format_decimal

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
	     <a href='/lastplayed' class='dropdown-toggle navbar-brand' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'>${ctx.djname} <span class='badge'>${format_decimal(ctx.dbstats.total_songs)}</span><span class='caret'></span></a>
	     <ul class='dropdown-menu'>
	      <li #{"class='active'" if resource == 'lastplayed' else ''}><a href='/lastplayed'>Last Played</a></li>
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
		 </ul>
		</li>
		<li class='dropdown
		: if resource in ('artist', 'album')
		 active
		: end
		'>
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
		#<li #{"class='active'" if resource == 'requests' else ''}>
		: using li_active resource, 'requests'
		 <a href='/requests'>Requests <span class='badge'><span id="requestbutton">${format_decimal(ctx.requests_info.request_count)}</span></span></a>
		: end
		#</li>
		: if ctx.new_counts.new_count > 0
		 <li #{"class='active'" if resource == 'whatsnew' else ''}>
		  <a href='/whatsnew'>New <span class='badge'>${format_decimal(ctx.new_counts.new_count)}</span></a>
		 </li>
		: end
		<li #{"class='active'" if resource == 'stats' else ''}><a href="/stats">Stats</a></li>
		<li><a href="#" data-toggle='modal' data-target='#suggestionModal'>Suggestion</a></li>
	   </ul>
	   <form class='navbar-form navbar-left' action='/search' method='post' role='search'>
	    <div class='form-group'>
	     <div class='input-group'>
	      <span class='input-group-addon'>
	       <li class='nav navbar-nav'>
	        <a href='#' data-toggle="modal" data-target='#searchModal'><span class='glyphicon glyphicon-search'></span></a>
	       </li>
	      </span>
	      <input type='hidden' class='form-comtrol' name='navbarsearch' placeholder='Search'>
	      <input type='text' class='form-comtrol' name='stext' placeholder='Search' style='height=25px'>
	     </div>
	    </div>
	   </form>
	   
	   <ul class='nav navbar-nav navbar-right'>
	    <li><a href="/admin"><span class='glyphicon glyphicon-cog'></span></a></li>
	    : if ctx.listeners is not None
			<li><a href='#'><span class='glyphicon glyphicon-headphones'></span> ${ctx.listeners.current}/${ctx.listeners.max}</a></li>
		: end
	   </ul>
	  </div>
	 </div>
	</nav>  
: end
