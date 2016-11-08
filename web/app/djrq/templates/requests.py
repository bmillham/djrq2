# encoding: cinje

: from .template import page
: from . import table_args, caption_args
: from .helpers.funcs import time_ago
: from .helpers.helpers import aa_link

: def requeststemplate title, ctx, requestlist
	: using page title, ctx, lang="en"
		<table #{table_args}>
		 <caption #{caption_args}>Current Requests</caption>
		 <tr><th>Artist</th><th>Album</th><th>Title</th><th>Requestor</th><th>Status</th><th>Last Requested</th></tr>
		 : for r in requestlist
			<tr>
			 : use aa_link r.song.artist, 'artist', td=True
			 : use aa_link r.song.album, 'album', td=True
			 <td>${r.song.title}</td>
			 <td>${r.name}</td>
			 <td>${r.status.capitalize()}</td>
			 <td>${time_ago(r.t_stamp)}</td>
			</tr>
		 : end
		</table>
	: end
: end
