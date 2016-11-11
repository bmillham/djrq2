# encoding: cinje

: from .template import page
: from .helpers.helpers import request_link, aa_link
: from .helpers.funcs import format_time, time_ago, format_decimal
: from . import table_args, caption_args

: def _tracklist title, ctx, a, r, songs
	 <table #{table_args}>
	  <caption #{caption_args}>${title}</caption>
	  <tr>
	   : if r == 'Album'
		   <th>Track #</th>
	   : end
	   <th>Title</th><th>Artist</th><th>Album</th><th>Length</th><th>Last Played</th></tr>
		: for i, row in enumerate(songs)
			<tr>
			 : if r == 'Album'
				 <td>${row.track}</td>
			 : end
			 : use request_link row, td=True
			 : use aa_link row.artist, 'artist', td=True
			 : use aa_link row.album, 'album', td=True
			 <td>${format_time(row.time)}</td>
			 <td>
			  : if len(row.played) > 0
				${time_ago(row.played[0].date_played)} by ${row.played[0].played_by}
				: if len(row.played) > 1
				 &nbsp;<span class="badge pull-right">${len(row.played)}</span>
				: end
			  : else
				&nbsp;
			  : end
			 </td>
			</tr>
			: if not (i % 100)
				: flush
			: end
		: end
	 </table>
: end

: def tracklist ctx, a, dataonly=False, phrase=None
	: if 'Query' in str(type(a))
		: print("Its a query")
		: c = a.count()
		: songs = a
		: n = 'Search'
	: else
	 : try
		: c = len(a.songs)
		: songs = a.songs
		: n = a.fullname
	 : except AttributeError
		: n = a[0]
		: c = a[1].count()
		: songs = a[1]
	 : end
	: end
	: try
		: r = ctx.resource.__resource__.capitalize()
	: except AttributeError
		: r = 'Search'
	: end
	: if phrase
		: title = "Found {} matches for {}".format(c, phrase)
	: else
		: title = "{} tracks {} {}: {}".format(format_decimal(c), 'on' if r == 'Album' else 'for', r, n)
	: end
	: if dataonly
		: use _tracklist title, ctx, a, r, songs
	: else
		: using page title, ctx, lang="en"
			: use _tracklist title, ctx, a, r, songs
		: end
	: end
: end
