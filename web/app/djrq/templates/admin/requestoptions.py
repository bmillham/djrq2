# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def requestoptionstemplate title, ctx, siteoptions=None, saved=False
    : using page title, ctx, lang="en"
        <div class='container'>
         <div class='row'>
          <div class='span12'>
           <form id='showinfoform' class='form-horizontal' action='/admin/requestoptions' method='post'>
            <fieldset>
             <legend>Request Options ${" [Saved]" if saved else ""}</legend>
             <input type='hidden' id='sid' name='sid' value='${siteoptions.id}'>
             <div class='form-group'>
                <label for='limit_requests'>Don't allow requests for tracks played by me within the last</label>
                <select class="form-control" id="limit_requests" name="limit_requests">
                    <option value='-1'>Never Allow Requests</option>
                    <option value='0'>Always Allow Requests</option>
                    <option value='1'>1 Hour</option>
                    : for i in range(2,24)
                     <option value='${i}' ${'selected' if i == siteoptions.limit_requests else ''}>${i} Hours</option>
                    : end
                </select>
             </div>
            </fieldset>
            <button type="submit" class="btn btn-primary" >Save</button>
           </form>
          </div>
         </div>
        </div>
    : end
: end
