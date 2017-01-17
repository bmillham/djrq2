# encoding: cinje

: from . import table_args
: from web.core.release import colophon
: from datetime import datetime

: def requestwindowtemplate1 title, ctx, requestinfo
    <table #{table_args}>
     <caption>Request: ${requestinfo.title}</caption>
      <tr><td>Artist</td><td>${requestinfo.artist.fullname}</td></tr>
      <tr><td>Album</td><td>${requestinfo.album.fullname}</td></tr>
      <tr><td>Title</td><td>${requestinfo.title}</td></tr>
    </table>
: end

: def sitenickinput ctx
 : nick = ctx.session.sitenick
 <label for='sitenick'>Your site nick</label>
 <input type='text'
        class='form-control sitenickinput'
        id='sitenick'
        name='sitenick'
        : if nick
         data-sitenick='${nick}'
         value='${nick}'
         disabled
        : end
        placeholder='Your site nick'
        required>
: end

: def requestmodal ctx
    <div class="modal fade" id="requestModal" tabindex="-1" role="dialog" aria-labelledby="requestModalLabel">
     <div class="modal-dialog" role="document">
      <div class="modal-content">
       <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
         <span aria-hidden="true">&times;</span>
        </button>
        <h4 class="modal-title" id="requestModalLabel">New Request</h4>
       </div>
       <div class="modal-body">
        <img id='ricon' style='display:none' src='/public/icons/horse_7.gif'>
        <div class="results">Results here</div>
        <form id='requestform' class='ajax' action='/requests' method='post' data-append='.results'>
         <input type='hidden' id='tid' name='tid'>
         <input type='hidden' id='formtype' name='formtype' value='request'>
         <div class='form-group'>
          : use sitenickinput ctx
          <label for='comment'>Comments</label>
          <input type="textarea" class="form-control" id="comment" name="comment" placeholder="Comments">
         </div>
         <button type="submit" class="btn btn-primary" >Submit Request</button>
         <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
        </form>
       </div>
      </div>
     </div>
    </div>
: end

: def mistagmodal ctx
    <div class="modal fade" id="mistagModal" tabindex="-1" role="dialog" aria-labelledby="mistagModalLabel">
     <div class="modal-dialog" role="document">
      <div class="modal-content">
       <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
         <span aria-hidden="true">&times;</span>
        </button>
        <h4 class="modal-title" id="mistagModalLabel">Report Mistag</h4>
       </div>
       <div class="modal-body">
        <img id='ricon' style='display:none' src='/public/icons/horse_7.gif'>
        <div class="results">Results here</div>
        <form id='mistagform' class='ajax' action='/requests' method='post' data-append='.results'>
         <input type='hidden' id='tid' name='tid'>
         <input type='hidden' id='formtype' name='formtype' value='mistag'>
         <div class='form-group'>
          : use sitenickinput ctx
          <label for='title'>Title</label>
          <input type='text' class='form-control' id='title' name='title'>
          <label for='artist'>Artist</label>
          <input type='text' class='form-control' id='artist' name='artist'>
          <label for='Album'>Album</label>
          <input type='text' class='form-control' id='album' name='album'>
          <label for='comment'>Comments</label>
          <input type="textarea" class="form-control" id="comment" name="comment" placeholder="Comments">
         </div>
         <button type="submit" class="btn btn-primary">Report Mistag</button>
         <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
        </form>
       </div>
      </div>
     </div>
    </div>
: end

: def suggestionmodal ctx
    <div class="modal fade" id="suggestionModal" tabindex="-1" role="dialog" aria-labelledby="suggestionModalLabel">
     <div class="modal-dialog" role="document">
      <div class="modal-content">
       <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
         <span aria-hidden="true">&times;</span>
        </button>
        <h4 class="modal-title" id="suggestionModalLabel">Suggest A Song</h4>
        <h6 class='modal-title' id='suggestionModalLabel'>Use this form to suggest a song that the DJ does not currently have</h6>
        <h6 class='modal-title' id='suggestionModalLabel'>Do not use the form to request a song! Use the Request buttons on the various pages.</h6>
       </div>
       <div class="modal-body">
        <img id='ricon' style='display:none' src='/public/icons/horse_7.gif'>
        <div class="results">Results here</div>
        <form id='suggestionform' class='ajax' action='/requests' method='post' data-append='.results'>
         <input type='hidden' id='formtype' name='formtype' value='suggestion'>
         <div class='form-group'>
          : use sitenickinput ctx
          <label for='title'>Title</label>
          <input type='text' class='form-control' id='title' name='title'>
          <label for='artist'>Artist</label>
          <input type='text' class='form-control' id='artist' name='artist'>
          <label for='Album'>Album</label>
          <input type='text' class='form-control' id='album' name='album'>
          <label for='comment'>Comments</label>
          <input type="textarea" class="form-control" id="comment" name="comment" placeholder="Comments">
         </div>
         <button type="submit" class="btn btn-primary">Make Suggestion</button>
         <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
        </form>
       </div>
      </div>
     </div>
    </div>
: end

: def infomodal ctx
    <div class="modal fade" id="infoModal" tabindex="-1" role="dialog" aria-labelledby="infoModalLabel">
     <div class="modal-dialog" role="document">
      <div class="modal-content">
       <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
         <span aria-hidden="true">&times;</span>
        </button>
        <h3><span class='glyphicon glyphicon-copyright-mark' aria-hidden='true'></span>&nbsp;2010-${datetime.now().year} Brian Millham</h3>
        <h4><i>This site is for informational purposes only. No music files are hosted or shared on this site</i></h4>
       </div>
       <div class="modal-body">
        #{colophon}
        <h6><b>Glyphicons:</b> <a href='http://glyphicons.com'>glyphicons.com</a></h6>
        <h6><b>Nginx:</b> <a href='http://nginx.com'>nginx.com</a></h6>
        <h6><b>SQLAlchemy:</b> <a href='http://sqlalchemy.org'>sqlalchemy.org</a></h6>
        <h6><b>MariaDB:</b> <a href='http://mariadb.com'>mariadb.com</a></h6>
        <h6><b>MongoDB:</b> <a href='http://mongodb.com'>mongodb.com</a></h6>
        <h6><b>HTML/css/js Famework:</b> <a href='http://getbootstrap.com'>Bootstrap</a></h6>
        <h6><b>Bootstrap Themes:</b> <a href='http://bootswatch.com'>Bootswatch</a></h6>
        <h3>Version Information</h3>
        <h6><b>Commit:</b> <a href='https://github.com/bmillham/djrq2/commit/${ctx.git_hexsha}'>${ctx.git_hexsha}</a> @ ${ctx.git_date}</h6>
        <h6><b>Committed by:</b> ${ctx.git_name}</h6>
        <h6><b>Commit Message:</b> ${ctx.git_message}</h6>
       </div>
      </div>
     </div>
    </div>
