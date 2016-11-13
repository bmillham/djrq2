# encoding: cinje

: from .template import page
: from . import table_args, caption_args
: from .helpers.funcs import time_ago, format_size, format_decimal, format_time, time_ago
: from .helpers.helpers import aa_link
: import datetime

: def whatsnewtemplate title, ctx, days, newlist
    : using page title, ctx, lang="en"
        <table #{table_args}>
         <caption #{caption_args}>${format_decimal(ctx.new_counts.new_count)} tracks added in the last ${time_ago(days, add_direction=False)}</caption>
         <tr><th>Artist</th><th>New Tracks</th><th>Size</th><th>Total Play Time</th><th>Date Added</th></tr>
         : for count, total_time, song_size, song in newlist
            <tr>
             : use aa_link song.artist, 'artist', td=True
             <td>${format_decimal(count)}</td>
             <td>${format_size(song_size)}</td>
             <td>${format_time(total_time)}</td>
             <td>${time_ago(datetime.datetime.fromtimestamp(song.addition_time))}</td>
            </tr>
         : end
        </table>
    : end
: end
