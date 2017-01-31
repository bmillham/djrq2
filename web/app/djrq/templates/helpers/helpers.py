#encoding: cinje

: from urllib.parse import quote_plus
: from time import mktime, time

: def request_link ctx, row, td=False, played=False, no_request_button=False
    : using _td td
        : try
         : lp = mktime(row.played[0].date_played.timetuple())
        : except
         : lp = 0
        : end
        : try
            : limit_requests = int(ctx.siteoptions.limit_requests)
        : except
            : limit_requests = -1
        : end
        : try
            : max_time = int(time()) - (limit_requests * 60 * 60)
        : except
            : max_time = 0
        : end
        #${row.title}
        : use truncate_title row.title
        <div class="pull-right">&nbsp;
         : if not no_request_button
          <button class="btn btn-xs btn-primary r_${row.id}"
                 id='r_${row.id}'
                 data-toggle="modal"
                 data-target="#requestModal"
                 data-title='${row.title}'
                 data-tid='${row.id}'
                 # Disable the button if there are requests
                 ${"disabled='disabled'" if len(row.new_requests) > 0 or lp > max_time or limit_requests == -1 or played else ""}
                 >
                 : if limit_requests == -1 and not played
                  No Requests
                : elif lp > max_time or played
                  Played
                : else
                  Request
                : end
          </button>
         : end
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

: def aa_link row, model, td=False, new_only=False -> strip
    : using _td td
        # Because 2 different database models are used, sometimes we get an
        # id back, sometimes an aid. And sometimes that id/aid is an int
        # but quote_plus doesn't like ints, so convert to string.
        : try
            : aid = str(row.id)
        : except
            : aid = str(row.aid)
        : end
        <a href='/${model}/?id=#{quote_plus(aid)}#{"&new_only" if new_only else ""}'>${row.fullname}</a>
    : end
: end

: def truncate_title title -> strip
    : if len(title) > 100
        #{title[:50]}...#{title[-50:]}
    : else
        ${title}
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
