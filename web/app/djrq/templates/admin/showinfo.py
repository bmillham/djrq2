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
             <div class='control-group'>
              <label class='control-label' for='showtitle'>Show Title</label>
              <div class='controls'>
               <input type='text' class='form-control' id='showtitle' name='showtitle' placeholder='Show Title' value='${showinfo.show_title}'>
              </div>
             </div>
             <div class='control-group'>
              <label class='control-label' for='showtime'>Show Time</label>
              <div class='controls'>
               <input type="datetime" class="form-control" id="showtime" name="showtime" placeholder="Show Start Time" value='${showinfo.show_time}'>
              </div>
             </div>
            </fieldset>
            <button type="submit" class="btn btn-primary" >Submit</button>
           </form>
          </div>
         </div>
        </div>
    : end
: end
