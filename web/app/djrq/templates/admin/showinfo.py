# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def showinfotemplate title, ctx, showinfo=None, saved=False
    : using page title, ctx, lang="en"
        <div class='container'>
         <div class='row'>
          <div class='span12'>
           <form id='showinfoform' class='form-horizontal' action='/admin/showinfo' method='post'>
            <fieldset>
             <legend>Show Information ${" [Saved]" if saved else ""}</legend>
             <input type='hidden' id='sid' name='sid' value='${showinfo.id}'>
             <div class='form-group'>
              <label class='control-label' for='show_title'>Show Title</label>
              <div class='controls'>
               <input type='text' class='form-control' id='show_title' name='show_title' placeholder='Show Title' value='${showinfo.show_title}'>
              </div>
             </div>
             <div class='form-group'>
              <label class='control-label' for='show_time'>Show Time</label>
              <div class='input-group date form_datetime' data-date-format="yyyy-mm-dd hh:ii z">
               <input type="text" class="form-control" readonly value='${showinfo.show_time}' name='show_time'>
               <span class="input-group-addon"><span class="glyphicon glyphicon-remove"></span></span>
               <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
              </div>
             </div>
            <h4>Both Show Title and Show Time must be set to have the show information display on the user pages</h4>
            </fieldset>
            <button type="submit" class="btn btn-primary" >Save</button>
           </form>
          </div>
         </div>
        </div>
    : end
: end
