# encoding: cinje

: from . import table_args

: def requestwindowtemplate1 title, ctx, requestinfo
		<table #{table_args}>
		 <caption>Request: ${requestinfo.title}</caption>
			<tr><td>Artist</td><td>${requestinfo.artist.fullname}</td></tr>
			<tr><td>Album</td><td>${requestinfo.album.fullname}</td></tr>
			<tr><td>Title</td><td>${requestinfo.title}</td></tr>
		</table>
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
	    #<form>
	     <input type='hidden' id='tid' name='tid'>
	     <input type='hidden' id='formtype' name='formtype' value='request'>
		 <div class='form-group'>
          <label for='sitenick'>Your site nick</label>
          <input type='text' class='form-control' id='sitenick' name='sitenick' required>
          <label for='comment'>Comments</label>
          <input type="textarea" class="form-control" id="comment" name="comment" placeholder="Comments">
         </div>
		 
         <button type="submit" class="btn btn-default" >Submit Request</button>
         #<a href="/requests" class="btn btn-default ajax" data-method='post' data-append='.results'>Submit Request</a>
         <button type="button" class="btn" data-dismiss="modal">Close</button>
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
          <label for='sitenick'>Your site nick</label>
          <input type='text' class='form-control' id='sitenick' name='sitenick' required>
          <label for='title'>Title</label>
          <input type='text' class='form-control' id='title' name='title'>
          <label for='artist'>Artist</label>
          <input type='text' class='form-control' id='artist' name='artist'>
          <label for='Album'>Album</label>
          <input type='text' class='form-control' id='album' name='album'>
          <label for='comment'>Comments</label>
          <input type="textarea" class="form-control" id="comment" name="comment" placeholder="Comments">
         </div>
         <button type="submit" class="btn btn-default">Report Mistag</button>
         <button type="button" class="btn" data-dismiss="modal">Close</button>
        </form>
	   </div>
	  </div>
	 </div>
	</div>
: end
