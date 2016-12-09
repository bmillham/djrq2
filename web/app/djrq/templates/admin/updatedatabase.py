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

: def updatedatabase title, ctx, files=[]
    : using page title, ctx, lang='en'
    <div class='container'>
    : use updateprogress
     <form id='updatedatabase' class='ajax' action='/admin/updatedatabase/updatedatabase' method='post' data-append='.results'>
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
      </fieldset>
      <button type='submit' class='btn btn-primary'>Update Database</button>
     </form>
    </div>
    : end
: end

: def updateprogress
    <div class='results'>Results here</div>
    <div class='progress'>
     <div class='progress-bar progress-bar-striped update-progress-bar' role='progressbar' aria-valuenow='0' aria-valuemin='0' aria-valuemax='100' style='min-width: 2em; width: 0%;'>
      0%
     </div>
    </div>
    <div class='backupprogress'><div>
    <div class='updateartist'></div>
    <div class='updatealbum'></div>
    <div class='updatetitle'></div>
    <div class='difference' id='difference'>
    <table class='table table-bordered table-striped vertical-table currenttrack-table' style='margin-left: auto; margin-right: auto; width: 100%;'>
     <tbody>
      <tr><th>File</th><th>Artist</th><th>Album</th><th>Title</th></tr>
      <tr><td class='currentfile'></td><td class='currentartist'></td><td class='currentalbum'></td><td class='currenttitle'></td></tr>
     </tbody>
    </table>
    <table class='table table-bordered table-striped vertical-table newtrack-table' style='margin-left: auto; margin-right: auto; width: 100%;'>
     <caption #{caption_args}>New Tracks <span class='badge updatedcount'>0</span></caption>
     <tbody>
      <tr><th>File</th><th>Artist</th><th>Album</th><th>Title</th></tr>
     </tbody>
    </table>
    <table class='table table-bordered table-striped vertical-table difftable' style='margin-left: auto; margin-right: auto; width: 100%;'>
     <caption #{caption_args}>Updated Tracks <span class='badge updatedcount'>0</span></caption>
     <tbody>
      <tr><th>File</th><th>Field</th><th>Original</th><th>Updated</th></tr>
     </tbody>
    </table>
    </div>
: end

: def updatecomplete ctx
    : print('Update complete:', ctx)
    : ctx.session.databaseupdating = False
    : return ctx
: end
