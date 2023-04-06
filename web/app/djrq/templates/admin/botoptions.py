# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def botoptionstemplate title, ctx, siteoptions=None, saved=False
    : using page title, ctx, lang="en"
        <div class='container'>
         <div class='row'>
          <div class='span12'>
           <form id='showinfoform' class='form-horizontal' action='/admin/botoptions' method='post'>
            <fieldset>
             <legend>Bot Options ${" [Saved]" if saved else ""}</legend>
             <input type='hidden' id='sid' name='sid' value='${siteoptions.id}'>
             <div class='form-group'>
                <label for='metadata_fields'>The metadata format that your stream software sends</label>
                <select class="form-control" id="metadata_fields" name="metadata_fields">
                    <option value='artist - title - album'
                     ${'selected' if ctx.siteoptions.metadata_fields == 'artist - title - album' else ''}>
                     Artist - Title - Album</option>
                    <option value='artist - title'
                    ${'selected' if ctx.siteoptions.metadata_fields == 'artist - title' else ''}>
                    Artist - Title</option>
                </select>
            </div>
            <div class='form-group'>
             <label for='strict_metadata'>Use Strict metadata</label>
             <select class='form-control' id='strict_metadata' name='strict_metadata'>
              <option value='1' ${'selected' if ctx.siteoptions.strict_metadata else ''}>
                Yes (recommended)</option>
              <option value='0' ${'selected' if not ctx.siteoptions.strict_metadata else ''}>
                No</option>
              </select>
            </div>
            <div class='form-group'>
             <label for='auto_update_requests'>Allow bot to update requests to played status</label>
             <select class='form-control' id='auto_update_requests' name='auto_update_requests'>
             <option value='1' ${'selected' if ctx.siteoptions.auto_update_requests else ''}>
              Yes
              </option>
            <option value='0'  ${'selected' if not ctx.siteoptions.auto_update_requests else ''}>
             No
             </option>
             </select>
             </div>
            <div class='form-group'>
             <label for='played_reporting_fields'><b>Played By</b> information to save</label>
             <select class='form-control' id='played_reporting_fields' name='played_reporting_fields'>
             : for o in ('dj', 'dj - show title', 'show title')
              <option value='${o}' ${'selected' if ctx.siteoptions.played_reporting_fields == o else ''}>${o.title()}</option>
             : end
            </option>
            </select>
            </div>
            <button type="submit" class="btn btn-primary" >Save</button>
           </form>
          </div>
         </div>
        </div>
    : end
: end
