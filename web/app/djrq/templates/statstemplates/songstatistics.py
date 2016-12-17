# encoding: cinje

: from ..helpers.funcs import format_decimal, format_size, format_percent, time_length, time_ago
: from .. import table_args, caption_args

: def songstatistics ctx
    : total_played_by_me = ctx.queries.get_total_played_by_me()
    : total_artists = ctx.queries.get_total_artists()
    : total_albums = ctx.queries.get_total_albums()

    <div class='table-responsive'>
        <table #{table_args}>
         <caption #{caption_args}>Song Statistics</caption>
         <tbody>
         <tr><td>Total Songs</td><td>${format_decimal(ctx.dbstats.total_songs)}</td></tr>
         <tr><td>Total Played By Me</td><td>${format_decimal(total_played_by_me.total)}
         ${format_percent(total_played_by_me.total / ctx.dbstats.total_songs)}
         </td></tr>
         <tr><td>Total Artists</td><td>${format_decimal(total_artists.total)}</td></tr>
         <tr><td>Total Albums</td><td>${format_decimal(total_albums.total)}</td></tr>
         <tr><td>Library Size</td><td>${format_size(ctx.dbstats.song_size)}</td></tr>
         <tr><td>Average Song Size</td><td>${format_size(ctx.dbstats.avg_song_size)}</td></tr>
         <tr><td>Total Song Playtime</td><td>${time_length(ctx.dbstats.song_time)}</td></tr>
         <tr><td>Average Song Length</td><td>${time_length(ctx.dbstats.avg_song_time)}</td></tr>
         </tbody>
        </table>
    </div>
: end
