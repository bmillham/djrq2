# encoding: cinje

: def searchwindow ctx
 <div id="searchModal" class="modal fade" role="dialog">
  <div class="modal-dialog">
   <div class="modal-content">
    <div class="modal-header">
     <button type="button" class="close" data-dismiss="modal">&times;</button>
     <h4 class="modal-title"> Advanced Search</h4>
    </div>
    <div class="modal-body">
     <p>You may use SQL % and _ wildcards</p>
     <img id='ricon' style='display:none' src='/public/icons/catgif8.gif'>
     <form id='searchform' action='/search' class='ajax' method='post' data-append='#main-content' role='search'>
      <div class='form-group'>
       <label for='advsearchtype'>Search For</label>
       <select class="form-control" id="advsearchtype" name="advsearchtype">
        <option>Artist</option>
        <option>Album</option>
        <option>Title</option>
       </select>
      </div>
      <input type="search" class="form-control" id="advsearchtext" name="advsearchtext" placeholder="Search">
     <button type="submit" class="btn btn-default">Search</button>
     <button type="button" class="btn" data-dismiss="modal">Close</button>
     </form>
    </div>
   </div>
  </div>
 </div>
: end 
