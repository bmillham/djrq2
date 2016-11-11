# encoding: cinje

: from .template import page
: from .helpers.helpers import request_link, aa_link
: from .helpers.funcs import format_decimal, format_size, format_percent, time_length, time_ago
: from . import table_args, caption_args

: def statstemplate title, ctx, stats_info
	: using page title, ctx, lang="en"
		<table #{table_args}>
		 <caption #{caption_args}>Song Statistics</caption>
		 <tbody>
		 <tr><td>Total Songs</td><td>${format_decimal(ctx.dbstats.total_songs)}</td></tr>
		 <tr><td>Total Played By Me</td><td>${format_decimal(stats_info['total_played_by_me'].total)}
		 ${format_percent(stats_info['total_played_by_me'].total / ctx.dbstats.total_songs)}
		 </td></tr>
		 <tr><td>Total Artists</td><td>${format_decimal(stats_info['total_artists'].total)}</td></tr>
		 <tr><td>Total Albums</td><td>${format_decimal(stats_info['total_albums'].total)}</td></tr>
		 <tr><td>Library Size</td><td>${format_size(ctx.dbstats.song_size)}</td></tr>
		 <tr><td>Average Song Size</td><td>${format_size(ctx.dbstats.avg_song_size)}</td></tr>
		 <tr><td>Total Song Playtime</td><td>${time_length(ctx.dbstats.song_time)}</td></tr>
		 <tr><td>Average Song Length</td><td>${time_length(ctx.dbstats.avg_song_time)}</td></tr>
		 </tbody>
		</table><br />
		<table #{table_args}>
		 <caption #{caption_args}>Top 10 Artists</caption>
		 <tr><th>#</th><th>Artist</th><th>Songs</th></tr>
		 : for c, r in enumerate(stats_info['top_10_artists'])
		  <tr>
		   <td>${c+1}</td>
			: use aa_link r, 'artist', td=True
		   <td>${format_decimal(r.artist_count)}</td>
		  </tr>
		 : end
		 </table><br />
		 : flush
		<table #{table_args}>
		 <caption #{caption_args}>10 Most Requested</caption>
		 <tr><th># Plays</th><th>Title</th><th>Artist</th><th>Album</th><th>Last Requested By</th></tr>
		 : for song in stats_info['10 Most Requested']
			<tr>
			 <td>${len(song.played_requests)}</td>
			  : use request_link song, td=True
			  : use aa_link song.artist, 'artist', td=True
			  : use aa_link song.album, 'album', td=True
			 <td>
			 : try
				${song.played_requests[0].name} ${time_ago(song.played_requests[0].t_stamp)}</td>
			 : except
				&nbsp;
			 : end
			</tr>
		 : end
		</table><br />
		: flush
		<table #{table_args}>
		 <caption #{caption_args}>Top 10 Requestors</caption>
		 <tr><th># Requests</th><th>Requestor</th><th>Last Request</th></tr>
		 : for r in stats_info['Top 10 Requestors']
		  <tr>
		   <td>${r.request_count}</td>
		   <td>${r.requestor}</td>
		   <td>${time_ago(r.last_request)}</td>
		  </tr>
		 : end
		</table><br />
		: flush
		<table #{table_args}>
		 <caption #{caption_args}>Top 10 Played By Me</caption>
		 <tr><th>Plays</th><th>Title</th><th>Artist</th><th>Album</th><th>Last Played</th></tr>
		 : for played in stats_info['10 Most Played By Me']
		  <tr>
		   <td>${played.played_count}</td>
		    : use request_link played.Played.song, td=True
		    : use aa_link played.Played.song.artist, 'artist', td=True
		    : use aa_link played.Played.song.album, 'album', td=True
		   <td>${time_ago(played.date_played)}</td>
		  </tr>
		 : end
		 </table><br />
		 : flush
		 <table #{table_args}>
		  <caption #{caption_args}>Top 10 Played By Other DJs</caption>
		  <tr><th>Plays</th><th>Title</th><th>Artist</th><th>Album</th><th>Last Played</th></tr>
		  : for played in stats_info['10 Most Played By Other DJs']
		   <tr>
		    <td>${played.played_count}</td>
		    : use request_link played.Played.song, td=True
		    : use aa_link played.Played.song.artist, 'artist', td=True
		    : use aa_link played.Played.song.album, 'album', td=True
		    <td>${time_ago(played.date_played)}</td>
		   </tr>
		  : end
		 </table><br />
		 : flush
		 <table #{table_args}>
		  <caption #{caption_args}>Top 10 Played By All DJs</caption>
		  <tr><th>Plays</th><th>Title</th><th>Artist</th><th>Album</th><th>Last Played</th></tr>
		  : for played in stats_info['10 Most Played By All DJs']
		   <tr>
		    <td>${played.played_count}</td>
		    : use request_link played.Played.song, td=True
		    : use aa_link played.Played.song.artist, 'artist', td=True
		    : use aa_link played.Played.song.album, 'album', td=True
		    <td>${time_ago(played.date_played)}</td>
		   </tr>
		  : end
		 </table><br />
	: end
: end
