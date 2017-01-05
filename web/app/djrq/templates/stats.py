# encoding: cinje

: from .template import page
: from .statstemplates.songstatistics import songstatistics
: from .statstemplates.topx import topx
: from .statstemplates.mostrequested import mostrequested
: from .statstemplates.toprequestors import toprequestors
: from .statstemplates.top10 import top10

: def statstemplate title, ctx, topartists=10
    : queries = ctx.queries
    : using page title, ctx, lang="en"
        <div class='container'>
         : if topartists == 10
          : use songstatistics ctx
         : end
          : use topx ctx, limit=topartists
         : flush
         : if topartists == 10
          : use mostrequested ctx
          : flush
          : use toprequestors ctx
          : flush
          : use top10 ctx, 'Top 10 Played By Me', queries.get_top_played_by(played_by_me=True)
          : flush
          : use top10 ctx, 'Top 10 Played By Other DJs', queries.get_top_played_by(played_by_me=False)
          : flush
          : use top10 ctx, 'Top 10 Played By All DJs', queries.get_top_played_by(played_by_me='all')
         : end
        </div>
    : end
: end
