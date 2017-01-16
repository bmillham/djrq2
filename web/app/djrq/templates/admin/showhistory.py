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
         : for c in commitlist
          : use gitline c
          : for s in ('files', 'lines', 'insertions', 'deletions')
           : totals[s] += c.stats.total[s]
          : end
         : end
         <tr><th colspan=4>Totals</th>
             <th>${totals['files']}</th>
             <th>${totals['lines']}</th>
             <th>${totals['insertions']}</th>
             <th>${totals['deletions']}</th>
         </tr>
         </table>
         </div>
         </div>
         </div>
    : end
: end

: def gitline commit, details=False
    <tr>
     : if not details
      <td><a href='/admin/showhistory/?commit=${commit.hexsha}'>${commit.hexsha[:7]}</a></td>
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
           <caption #{caption_args}>Details for commit <a href='https://github.com/bmillham/djrq2/commit/${commit.hexsha}' target='_blank' rel='noopener noreferrer'>${commit.hexsha}</a></caption>
           <tr>
            <th rowspan=2>Committer</th>
            <th rowspan=2>Date</th>
            <th rowspan=2>Message</th>
            <th colspan=4>Change Summary</td>
           </tr>
           <tr>
            <th>Files</th><th>Lines</th><th>Insertions</th><th>Deletions</th>
           </tr>
          : use gitline commit, details=True
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
