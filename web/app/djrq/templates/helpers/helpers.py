#encoding: cinje

: from urllib.parse import quote_plus
: from time import mktime, time

: def request_link ctx, row, td=False
    : using _td td
        : try
         : lp = mktime(row.played[0].date_played.timetuple())
        : except
         : lp = 0
        : end
        : max_time = int(time()) - (int(ctx.siteoptions.limit_requests) * 60 * 60)
        ${row.title}
        <div class="pull-right">
         <button class="btn btn-xs btn-primary r_${row.id}"
                 id='r_${row.id}'
                 data-toggle="modal"
                 data-target="#requestModal"
                 data-title='${row.title}'
                 data-tid='${row.id}'
                 # Disable the button if there are requests
                 ${"disabled='disabled'" if len(row.new_requests) > 0 or lp > max_time or ctx.siteoptions.limit_requests == -1 else ""}
                 >
                 : if ctx.siteoptions.limit_requests == -1
                  No Requests
                : elif lp > max_time
                  Played
                : else
                  Request
                : end
         </button>
         <button class="btn btn-xs btn-info m_${row.id}"
                 id='m_${row.id}'
                 data-toggle='modal'
                 data-target='#mistagModal'
                 data-title='${row.title}'
                 data-artist='${row.artist.fullname}'
                 data-album='${row.album.fullname}'
                 data-tid='${row.id}'
                 ${"disabled='disabled'" if len(row.mistags) > 0 else ""}
                 >Mistag
         </button>
        </div>
    : end
: end

: def aa_link row, model, td=False -> strip
    : using _td td
        # Because 2 different database models are used, sometimes we get an
        # id back, sometimes an aid. And sometimes that id/aid is an int
        # but quote_plus doesn't like ints, so convert to string.
        : try
            : aid = str(row.id)
        : except
            : aid = str(row.aid)
        : end
        <a href='/${model}/?id=#{quote_plus(aid)}'>${row.fullname}</a>
    : end
: end

: def _td use_td
    : if use_td
        <td>
    : end
    : yield
    : if use_td
        </td>
    : end
: end
