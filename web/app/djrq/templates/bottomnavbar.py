# encoding: cinje
: from datetime import datetime
: import pytz
: def bottomnavbar ctx
 <nav class='navbar navbar-default navbar-inverse navbar-fixed-bottom'>
  <div class='container-fluid'>
   <div class='collapse navbar-collapse' id='collapse-2'>
    <a class='navbar-brand' href='#'>Show Title: ${ctx.siteoptions.show_title}</a>
    <p class='navbar-text'>&nbsp;&nbsp;</p>
    <a class='navbar-brand' href='#'>
     : time_ago, secs_ago = ctx.time_ago(ctx.siteoptions.show_time, return_diff=True)
     : if secs_ago > 0
      Show Time
     : else
      Show Started
     : end
      ${time_ago} @ ${ctx.siteoptions.show_time}
    </a>
    <p class='navbar-right navbar-text'>
     <span class='glyphicon glyphicon-copyright-mark' aria-hidden='true'></span>
     &nbsp;2010-${datetime.now().year} Brian Millham&nbsp;
    </p>
   </div>
  </div>
 </nav>
: common = pytz.common_timezones
: dt = datetime.strptime(ctx.siteoptions.show_time, '%Y-%m-%d %H:%M %z')
#: for c in pytz.country_names
#    : try
#        : print(c, pytz.country_names[c], pytz.country_timezones[c])
#    : except
#        : print('No timezone for {}'.format(c))
#    : else
#        : for z in pytz.country_timezones[c]
#            : print(z, dt.astimezone(pytz.timezone(z)).strftime('%Y-%m-%d %H:%M %Z [%z]'))
#        : end
#    : end
#: end
 #: print(ctx.siteoptions.showtime.replace(tz
: end
