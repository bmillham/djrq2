# encoding: cinje

: from .template import page
: from . import table_class, table_style, caption_args
: from .helpers.helpers import aa_link
: import datetime

: def whatsnewtemplate title, ctx, days, newlist
    : using page title, ctx, lang="en"
        <div class='container'>
        <div class='row table-responsive'>
         <div class="col-md-12">
        : table_class.append('sortable')
        <table class="#{' '.join(table_class)}" style="#{' '.join(table_style)}" id='whatsnew'>
         <caption #{caption_args}>${ctx.format_decimal(ctx.new_counts.new_count)} tracks added in the last ${ctx.time_ago(days, add_direction=False)}</caption>
         <thead>
         <tr><th>Artist</th><th>New Tracks</th><th>Size</th><th>Total Play Time</th><th>Date Added</th></tr>
         </thead>
         <tbody>
         : for count, total_time, song_size, song in newlist
            <tr>
             : use aa_link song.artist, 'artist', td=True, new_only=True
             <td data-value='${count}'>${ctx.format_decimal(count)}</td>
             <td data-value='${song_size}'>${ctx.format_size(song_size)}</td>
             <td data-value='${total_time}'>${ctx.format_time(total_time)}</td>
             <td data-value='${song.addition_time}'>${ctx.time_ago(datetime.datetime.fromtimestamp(song.addition_time))}</td>
            </tr>
         : end
         </tbody>
        </table>
        </div>
        </div>
        </div>
    : end
: end
