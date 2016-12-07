#encoding: cinje

: from .admintemplate import page
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
    <div class='results' style='display: none'>Results here</div>
    <div class='backupprogress'><div>
: end

: def updatecomplete ctx
    : print('Update complete:', ctx)
    : ctx.session.databaseupdating = False
    : return ctx
: end
