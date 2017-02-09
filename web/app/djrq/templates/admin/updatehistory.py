#encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args
: import os

: def selectfile title, ctx, files=[]
    : using page title, ctx, lang="en"
    <div class='container'>
        <form action='/admin/updatehistory/view' method='post'>
         <fieldset>
          <legend>File Selection</legend>
          <div class='form-group'>
           <label for='fileselection'>Select database update to view</label>
           <select class="form-control" id="fileselection" name="fileselection">
           : for f in files
            <option value='${os.path.split(f)[-1]}'>${os.path.split(f)[-1]}</option>
           : end
           </select>
          </div>
         </fieldset>
         <button type="submit" class="btn btn-primary" >View Update History</button>
        </form>
    </div>
    : end
: end

: def updatehistorysummary title, ctx, summary, fn
    : using page title, ctx, lang='en'
    <div class='container'>
     <table class='table table-bordered table-striped vertical-table stats-table' style='margin-left: auto; margin-right: auto; width: 100%;'>
      <caption #{caption_args}>Update Summary For ${fn}</caption>
      <tr><th>Type</th><th>Count</th></tr>
     : details = {'empty': 'Tracks that are missing artist/album or title tags',
     :            'space': 'Tracks that have extra spaces in the artist/album or title tags',
     :            'dash': 'Tracks that have dash (surrounded by spaces) in artist/album or title tags'}
     : for r in summary
      <tr>
       <td>${details[r]}</td>
       <td><a href='/admin/updatehistory/view?fileselection=${fn}&details=${r}'>${summary[r]}</a></td>
      </tr>
     : end
     </table>
    </div>
    : end
: end

: def updatehistorydetails title, ctx, details, args
    : using page title, ctx, lang='en'
    : fields = ('artist', 'album', 'title', 'path', 'filename')

    <div class='container'>
     <table class='table table-bordered table-striped vertical-table stats-table' style='margin-left: auto; margin-right: auto; width: 100%;'>
      <caption #{caption_args}>Update Details For ${args['details']}</caption>
      <tr>
       : for f in fields
        <th>${f.capitalize()}</th>
       : end
      </tr>
     : for r in details
      <tr>
       : to_report = {}
       : for f in fields
        <td>
         : if args['details'] == 'space' and f in ('artist', 'album', 'title')
          : rf = r[f]
          : if rf is None
           : rf = ''
          : end
          : if rf != ' '.join(rf.split())
           : to_report[f] = rf.replace(' ', '<b>_</b>')
          : end
          : for k in to_report
           <td>${k}</td><td>#{to_report[k]}</td>
          : end
         : else
          ${r[f]}
         : end
        </td>
       : end
      </tr>
     : end
     </table>
    </div>
    : end
: end

: def emptymessage
    <h1>Tracks that were ignored because a required tag was missing</h1>
: end

: def spacemessage
    <h1>Tags With Extra Spaces</h1>
    <h4>You should look into fixing these tags, as they may cause problems while you are DJing.
        The Shoutcast server may strip this tags, but not always. So tracks that you play may
        not be automatically found.
    </h4>
    <h5>To make it easier to spot the problems, spaces in the original tags are displayed as _</h5>
: end

: def dashmessage
    <h1>Tags With Dashes</h1>
    <h4>These tags have a -, surrounded by spaces in them. These are bad because they make it
        impossible for the track to be automatically marked as played.</h4>
    <h5>An example of the problem. Take the track tagged:
        <ul>
         <li>Artist: The Shat</li>
         <li>Album: The Horrible - Horrible Songs</li>
         <li>Title: The Shat Does - Wing</li>
        </ul>
        The script that reads from the Shoutcast server expects tracks to be either
        <ul>
         <li>Artist - Track</li>
         <li>Artist - Album - Track</li>
        </ul>
        But the above example would be
        <ul>
         <li>The Shat - The Horrible - Horrible Songs - The Shat Does - Wing</li>
         <li>The Shat - The Shat Does - Wing.</li>
        </ul>
        <p>See the problem? Neither matches what you actually played.<p>
        <p>Please remove the spaces around the - in these tracks. It is OK to have Artist- Title or Artist -Title, just as long as the - does not have spaces before and after.</p>
    </h5>
: end

: def updatehistoryspace title, ctx, details, cursor, args
    : using page title, ctx, lang='en'
    : fields = ('artist', 'album', 'title', 'path', 'filename')

    <div class='container'>
     : if args['details'] == 'space'
      : use spacemessage
     : end
     : if args['details'] == 'dash'
      : use dashmessage
     : end
     : if args['details'] == 'empty'
      : use emptymessage
     : end
     <table class='table table-bordered table-striped vertical-table stats-table' style='margin-left: auto; margin-right: auto; width: 100%;'>
      <tr><th>Field</th>
          : if args['details'] == 'space'
           <th>Fixed Tag</th>
           <th>Original Tag</th>
          : elif args['details'] == 'dash'
           <th>Tag</th>
          : end
          <th>Path</th>
          <th>Filename</th>
      </tr>
     : ids = {}
     <tbody>
     : for r in details
      : ids[r['id']] = r['fcount']
     : end
     : for i1, r in enumerate(ids)
      : for i, d in enumerate(cursor.execute('select * from fixedtable where recordtype=:rtype and id=:tid', {'rtype': args['details'], 'tid': r}))
      <tr>
        <td>${d['field'].capitalize()}</td>
        : if args['details'] == 'space'
         <td>${d['val']}</td>
         <td>#{d['oval'].replace(' ', ' <b>_</b> ')}</td>
        : elif args['details'] == 'dash'
         <td>${d['oval']}</td>
        : end
        : if i == 0
         <td rowspan="#{ids[r]}">${d['path']}</td><td rowspan="#{ids[r]}">${d['filename']}</td>
        : end
       </tr>
      : end
      : if not (i1 % 49) and i1 != 0
         </tbody>
        : flush
        <tbody>
        : end
     : end
     </tbody>
     </table>
    </div>
    : end
: end