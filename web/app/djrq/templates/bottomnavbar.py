# encoding: cinje
: from datetime import datetime

: def bottomnavbar ctx
 <nav class='navbar navbar-default navbar-inverse navbar-fixed-bottom'>
  <div class='container-fluid'>
   <div class='collapse navbar-collapse' id='collapse-2'>
    <a class='navbar-brand' href='#'>Show Title: ${ctx.siteoptions.show_title}</a>
    <p class='navbar-text'>&nbsp;&nbsp;</p>
    <a class='navbar-brand' href='#'>Show Time: ${ctx.siteoptions.show_time}</a>
    <p class='navbar-right navbar-text'>
     <span class='glyphicon glyphicon-copyright-mark' aria-hidden='true'></span>
     &nbsp;2010-${datetime.now().year} Brian Millham&nbsp;
    </p>
   </div>
  </div>
 </nav>
: end
