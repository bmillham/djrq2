# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args

: def authtemplate title, ctx, requestlist
    : using page title, ctx, lang="en"
        <div class='container'>
         <div class='row'>
          <div class='span12'>
           <form id='loginform' class='form-horizontal' action='/admin/auth' method='post'>
            <fieldset>
             <legend>Please Login</legend>
             <div class='control-group'>
              <label class='control-label' for='username'>User Name</label>
              <div class='controls'>
               <input type='text' maxlength='50' class='form-control' id='username' name='username' placeholder='User Name'>
              </div>
             </div>
             <div class='control-group'>
              <label class='control-label' for='password'>Password</label>
              <div class='controls'>
               <input type="password" maxlength='50' class="form-control" id="password" name="password" placeholder="Password">
              </div>
             </div>
            </fieldset>
            <button type="submit" class="btn btn-primary" >Login</button>
           </form>
          </div>
         </div>
        </div>
        #<a href='/admin/auth/?user=bmillham'>Login</a>
    : end
: end
