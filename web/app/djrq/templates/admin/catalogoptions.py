# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args
: from datetime import datetime

: def catalogoptionstemplate title, ctx, cats=None, saved=False
    : using page title, ctx, lang="en"
        <div class='container'>
         <div class='row'>
          <div class='span12'>
           <form id='catalogform' class='form-horizontal' action='/admin/catalogoptions' method='post'>
            <fieldset>
             <legend>Catalog Selection ${" [Saved]" if saved else ""}</legend>
             <input type='hidden' id='sid' name='sid' value='${ctx.siteoptions.id}'>
              <table class="table table-bordered table-striped table-condensed">
               <tr>
                <th>Enabled</th>
                <th>Catalog</th>
                <th>Last Update</th>
               </tr>
               : for cat in cats
                <tr>
                <td><input ${'checked' if str(cat.id) in ctx.siteoptions.catalog.split(',') else ''}
                           class='form-control input-sm' type='checkbox' name='cat_group' value='${cat.id}'></td>
                <td>${cat.name}</td>
                <td>${ctx.time_ago(datetime.fromtimestamp(cat.last_add))}</td>
                </tr>
               : end
             </table>
            </fieldset>
            <button type="submit" class="btn btn-primary" >Save</button>
           </form>
          </div>
         </div>
        </div>
    : end
: end
