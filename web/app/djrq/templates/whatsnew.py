# encoding: cinje

: from .template import page
: from . import table_args, caption_args
: from .helpers.helpers import aa_link
: import datetime

: def whatsnewtemplate title, ctx, days, newlist
    : using page title, ctx, lang="en"
        <div class='container'>
        <div class='table-responsive'>
        <table #{table_args}>
         <caption #{caption_args}>${ctx.format_decimal(ctx.new_counts.new_count)} tracks added in the last ${ctx.time_ago(days, add_direction=False)}</caption>
         <tr><th>Artist</th><th>New Tracks</th><th>Size</th><th>Total Play Time</th><th>Date Added</th></tr>
         : for count, total_time, song_size, song in newlist
            <tr>
             : use aa_link song.artist, 'artist', td=True
             <td>${ctx.format_decimal(count)}</td>
             <td>${ctx.format_size(song_size)}</td>
             <td>${ctx.format_time(total_time)}</td>
             <td>${ctx.time_ago(datetime.datetime.fromtimestamp(song.addition_time))}</td>
            </tr>
         : end
        </table>
        </div>
        </div>
    : end
: end
