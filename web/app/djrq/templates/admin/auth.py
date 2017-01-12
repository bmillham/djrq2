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
    : end
: end

: def change_pw_template title, ctx, first_access=False, status_message=None
    : using page title, ctx
        <div class='container'>
         <div class='row'>
          <div class='span12'>
           <form id='changepwform' class='form-horizontal' action='/admin/changepw' method='post'>
            <fieldset>
             <legend>
              : if status_message
                ${status_message}
              : elif first_access
               Password security has been updated on the site. It is recommended that you change your password.
              : else
               Changing Password
              : end
             </legend>
             <div class='control-group'>
              <label class='control-label' for='currentpw'>Current Password</label>
              <div class='controls'>
               <input type='password' maxlength='50' class='form-control' id='currentpw' name='currentpw' placeholder='Current Password'>
              </div>
             </div>
             <div class='control-group'>
              <label class='control-label' for='newpw'>New Password <span id='np-label' style='color:red'></span></label>
              <div class='controls'>
                <input type='password' maxlength='50' class='form-control' id='newpw' name='newpw' required placeholder='New Password'>
              </div>
             </div>
             <div class='control-group'>
              <label class='control-label' for='repeatnewpw'>Repeat New Password</label>
              <div class='controls'>
                <input type='password' maxlength='50' class='form-control' id='repeatnewpw' name='repeatnewpw' required placeholder='Repeat New Password'>
              </div>
             </div>
            </fieldset>
            <button type='submit' class='btn btn-primary'>Change Password</button>
           </form>
          </div>
         </div>
        </div>
    : end
: end
