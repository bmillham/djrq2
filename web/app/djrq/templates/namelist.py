# encoding: cinje
: from . import table_args, caption_args

: def namelist ctx, names
	 <table #{table_args}>
  	: resource = ctx.resource.__resource__
	  <caption #{caption_args}>Browsing by ${resource.capitalize()} (${ctx.selected_letter})</caption>
#	  <tr><th>Fullname</th><th>Track Count</th></tr>
		: i = 0
		: row_ended = False
		: rows = 3
		: for row in names
		:	if i % rows == 0
		:	 row_ended = False
			<tr>
		:   end
			 <td>
			  <a href="/${resource}/?id=${row.aid}">${row.fullname}</a>&nbsp;<span class="badge pull-right">${row.songcount}</span>
			 </td>
		:   if i % rows == rows - 1
		:	 row_ended = True
			</tr>
		:   end
		:   i += 1
		: end
		: if not (i % 15)
			:flush
		: end
		: if not row_ended
		:	i -= 1
		:	while i % rows != rows - 1 and i > rows - 1
			<td>&nbsp;</td>
		:	i += 1
		:   end
			</tr>
		: end
	 </table>
: end
