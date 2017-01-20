# encoding: cinje

: from .admintemplate import page
: from .. import table_args, caption_args
: import time

: def showhistorytemplate title, ctx, commitlist
    : using page title, ctx, lang="en"
        <div class='container'>
        <div class="row table-responsive">
         <div class="col-md-12">
        <table #{table_args}>
         <caption #{caption_args}>Site Change History <span class='label label-primary'>${ctx.git_total_commits} Commits</span></caption>
         <tr>
          <th rowspan=2>Commit ID</th>
          <th rowspan=2>Committer</th>
          <th rowspan=2>Date</th>
          <th rowspan=2>Message</th>
          <th colspan=4>Change Summary</td>
         </tr>
         <tr>
          <th>Files</th><th>Lines</th><th>Insertions</th><th>Deletions</th>
         </tr>
         : totals = {'files': 0,
         :           'lines': 0,
         :           'insertions': 0,
         :           'deletions': 0,}
         <tbody>
         : flush
         : starttime = time.time()
         : for i, c in enumerate(commitlist)
          #: use gitline ctx, c
          : yield from gitline(ctx, c)
          #: for s in ('files', 'lines', 'insertions', 'deletions')
          # : totals[s] += c.stats.total[s]
          #: end
          #: totals['files'] += c.stats.total['files']
          : if not (i % 24) and i != 0
           </tbody>
           : flush
           <tbody>
          : end
         : end
         : totaltime = time.time() - starttime
         : print('Time generating list', totaltime)
         <tr><th colspan=4>Totals</th>
             <th>${ctx.git_totals['files']}</th>
             <th>${ctx.git_totals['lines']}</th>
             <th>${ctx.git_totals['insertions']}</th>
             <th>${ctx.git_totals['deletions']}</th>
         </tr>
         </tbody>
         </table>
         </div>
         </div>
         </div>
    : end
: end

: def gitline ctx, commit, details=False -> strip
    <tr>
     : if not details
      <td><a href='/admin/showhistory/?commit=${commit.hexsha}'>
           : if commit.hexsha in ctx.git_tags
            <b>${ctx.git_tags[commit.hexsha]}</b>
           : else
            ${commit.hexsha[:7]}
           : end
          </a>
      </td>
     : end
     <td>${commit.committer.name}</td>
     <td>${time.strftime("%Y-%m-%d %H:%M:%S %z", time.gmtime(commit.committed_date))}</td>
     <td>${commit.message}</td>
     : for s in ('files', 'lines', 'insertions', 'deletions')
      <td>
       ${commit.stats.total[s]}
      </td>
     : end
    </tr>
: end

: def showdetails title, ctx, commit
     : using page title, ctx, lang="en"
       <div class='container'>
        <div class="row table-responsive">
         <div class="col-md-12">
          <table #{table_args}>
           <caption #{caption_args}>
            Details for
             : args = {'href': 'https://github.com/bmillham/djrq2/commit/' + commit.hexsha,
             :         'target': '_blank',
             :         'rel': 'noopener noreferrer'}
             : if commit.hexsha in ctx.git_tags
              release <a &{args}>${ctx.git_tags[commit.hexsha]}</a>
             : else
              commit <a &{args}>${commit.hexsha}</a>
             : end
           </caption>
           <tr>
            <th rowspan=2>Committer</th>
            <th rowspan=2>Date</th>
            <th rowspan=2>Message</th>
            <th colspan=4>Change Summary</td>
           </tr>
           <tr>
            <th>Files</th><th>Lines</th><th>Insertions</th><th>Deletions</th>
           </tr>
          : use gitline ctx, commit, details=True
          </table>
          <table #{table_args}>
           <caption #{caption_args}>Files Changed</caption>
           <tr>
            <th>File</th><th>Lines</th><th>Insertions</th><th>Deletions</th>
           </tr>
           : for f in commit.stats.files
           <tr>
            <td>${f}</td>
            : for col in ('lines', 'insertions', 'deletions')
             <td>${commit.stats.files[f][col]}</td>
            : end
           </tr>
           : end
          </table>
         </div>
        </div>
      </div>
    : end
: end
