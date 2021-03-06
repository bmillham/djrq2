#encoding: cinje

: from ..helpers.helpers import request_link, aa_link
: from .. import table_args, caption_args

: def top10 ctx, title, query
 <div class='table-responsive'>
  <table #{table_args}>
  <caption #{caption_args}>${title}</caption>
   <tr><th>Plays</th><th>Title</th><th>Artist</th><th>Album</th><th>Last Played</th></tr>
   : for played in query
    <tr>
     <td>${played.played_count}</td>
     : use request_link ctx, played.Played.song, td=True
     : use aa_link played.Played.song.artist, 'artist', td=True
     <td>
     : albums = ctx.queries.get_multi_albums(played.Played.song.artist.fullname, played.Played.song.title)
     : if albums.count() > 1
        <span data-html='1' data-toggle='popover' data-placement='right auto' data-trigger='hover' title="On ${albums.count()} albums" data-content="
        : for a in albums
            ${a.album.fullname}<br />
        : end
        ">On ${albums.count()} albums</span>
     : else
        : use aa_link played.Played.song.album, 'album'
     : end
     </td>
     <td>${ctx.time_ago(played.date_played)}</td>
    </tr>
   : end
  </table>
 </div>
: end
