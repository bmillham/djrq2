# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def mistagstemplate title, ctx, mistaglist
    : using page title, ctx, lang="en"
        <div class='container'>
        <div class="row table-responsive">
         <div class="col-md-12">
        <table #{table_args}>
         <caption #{caption_args}>Mistags</caption>
         <tr>
          <th>Action</th>
          <th colspan=2>Artist</th>
          <th colspan=2>Album</th>
          <th colspan=2>Title</th>
          <th>Reported By</th>
          <th>Reported</th>
          <th>Comments</th>
          <th>Filename</th>
         </tr>
         : for r in mistaglist
          <tr>
           <td rowspan=2><a href='/admin/mistags/?delete=${r.id}' class='btn btn-xs btn-primary'>Delete Mistag</a></td>
           : if r.song.artist.fullname == r.artist
            <td colspan=2 rowspan=2>${r.song.artist.fullname}</td>
           : else
            <td>Original</td><td>${r.song.artist.fullname}</td>
           : end
           : if r.song.album.fullname == r.album
            <td colspan=2 rowspan=2>${r.song.album.fullname}</td>
           : else
            <td>Original</td><td>${r.song.album.fullname}</td>
           : end
           : if r.song.title == r.title
            <td rowspan=2 colspan=2>${r.song.title}</td>
           : else
            <td>Original</td><td>${r.song.title}</td>
           : end
           <td rowspan=2 >${r.reported_by}</td>
           <td rowspan=2>${r.reported}</td>
           <td rowspan=2>${r.comments}</td>
           <td rowspan=2>${r.song.file}</td>
          </tr>
          <tr>
           : if r.song.artist.fullname != r.artist
            <th>Corrected</th><th>${r.artist}</th>
           : end
           : if r.song.album.fullname != r.album
            <th>Corrected</th><th>${r.album}</th>
           : end
           : if r.song.title != r.title
            <th>Corrected</th><th>${r.title}</th>
           : end
          </tr>
         : end
         </table>
         </div>
         </div>
         </div>
    : end
: end
