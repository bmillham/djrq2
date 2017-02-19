#encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args
: import os

: def selectfile title, ctx, files=[]
    : using page title, ctx, lang="en"
    <div class='container'>
        <form action='/admin/updatedatabase/unpack' method='post'>
         <fieldset>
          <legend>File Selection</legend>
          <div class='form-group'>
           <label for='fileselection'>Select a file to unpack</label>
           <select class="form-control" id="fileselection" name="fileselection">
           : for f in files
            <option value='${os.path.split(f)[-1]}'>${os.path.split(f)[-1]}</option>
           : end
           : if len(files) == 0
            <option value='uncompressed'>I uploaded an uncompressed file</option>
           : end
           </select>
           <label for='backupdb'>Backup your database? (recommended)</label>
           <input type='checkbox' name='backupdb' value='1' checked>
          </div>
         </fieldset>
         <button type="submit" class="btn btn-primary" >Unpack</button>
        </form>
    </div>
    : end
: end

: def selectdatabasefile title, ctx, files=[]
    : using page title, ctx, lang='en'
    <div class='container'>
     <form id='updatedatabase-form' class='ajax' style='#{'display: none' if ctx.queries.is_updating() else ''}' action='/admin/updatedatabase/updatedatabase' method='post'>
      <fieldset>
       <legend>Update Database</legend>
       <div class='form-group'>
        <label for='fileselection'>Select the database main or xml file</label>
        <select class='form-control' id='fileselection' name='fileselection'>
        : for f in files
         <option value='${os.path.split(f)[-1]}'>${os.path.split(f)[-1]}</option>
        : end
        </select>
       </div>
       <div>
        <label for='stripspaces'>Remove Extra Spaces From Artist/Album/Title?</label>
        <input type='checkbox' id='stripspaces' name='stripspaces' value='1' checked>
       </div>
       <div>
        <label>Replace Empty Tags With Unknown? (if not selected, tracks with empty tags will <i>not</i> be added to the database)</label>
        <label for='artisttagfix'>Artist</label>
        <input type='checkbox' id='artisttagfix' name='artisttagfix' value='1'>
        <label for='albumtagfix'>Album</label>
        <input type='checkbox' id='albumtagfix' name='albumtagfix' value='1' checked>
        <label for='titletagfix'>Title</label>
        <input type='checkbox' id='titletagfix' name='titletagfix' value='1' checked>
       </div>
      </fieldset>

      <button type='submit' class='btn btn-primary'>Update Database</button>
     </form>
     : use updateprogress title, ctx
    </div>
    : end
: end

: def updateprogress title, ctx
    <div id='progress-div' style='#{'display: none' if not ctx.queries.is_updating() else ''}'>
     <div class='row'>
        <div class='col-sm-11 col-lg-11'><h3><span id='stage'>Preparing To Update</span>
         <a style='display:none' id='historyfilename' href='#'>View Update Details</a></h3>
        </div>
        <div class='col-sm-1 col-lg-1'><img src='/public/icons/horse_7.gif' id='spinner' alt='spinner' style='top: 20px; width:30px; height: 30px; position: relative;' /></div>
     </div>
     <div class='progress'>
      <div id='progress' class='progress-bar progress-bar-striped update-progress-bar' role='progressbar' aria-valuenow='0' aria-valuemin='0' aria-valuemax='100' style='min-width: 2em; width: 0%;'>
       0%
      </div>
     </div>
     <div class='stats'>
      <table class='table table-bordered table-striped vertical-table stats-table' style='margin-left: auto; margin-right: auto; width: 100%;'>
       <caption #{caption_args}>Update Statistics</caption>
       <tbody>
        <tr><th rowspan=2>Ave. Time</th><th colspan=4>Tracks</th><th colspan=4>Deleted</th></tr>
        <tr><th>Total</th><th>Checked</th><th>Added</th><th>Updated</th><th>Tracks</th><th>Played</th><th>Requests</th><th>Mistags</th></tr>
        <tr><td id='avetime'>0</td><td id='totaltracks'>0</td><td id='checkedtracks'>0</td><td id='addedtracks'>0</td><td id='updatedtracks'>0</td>
            <td id='deletedtracks'>0</td><td id='deletedplayed'>0</td><td id='deletedrequests'>0</td><td id='deletedmistags'>0</td></tr>
       </tbody>
      </table>
     </div>
    </div>
: end
