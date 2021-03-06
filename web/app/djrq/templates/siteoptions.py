# encoding: cinje

: from .template import page

: def siteoptionstemplate title, ctx, updated=False
    : using page title, ctx, lang="en"
        <h3 style='text-align: center;'>Site Options ${'(Saved)' if updated else ''}</h3>
        <form style='width: 50vw; margin: 0 auto;' action='/siteoptions' method='post'>
         <div class='form-group'>
          <label for='theme'>Select A Theme</label>
          <select class='form-control' id='theme' name='theme'>
          : for t in sorted(ctx.themes.keys())
           <option ${'selected' if t == ctx.usertheme else ''}>${t}</option>
          : end
          </select>
         </div>
         <button type='submit' class='btn btn-default'>Change Options</button>
        </form>
    : end
: end
