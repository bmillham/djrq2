# encoding: cinje

: def bottomnavbar ctx
 <nav class='navbar navbar-default navbar-inverse navbar-fixed-bottom'>
  <div class='container-fluid'>
   <div class='collapse navbar-collapse' id='collapse-2'>
    <a class='navbar-brand' href='#'>Show Title: ${ctx.siteoptions.show_title}</a>
    <a class='navbar-right navbar-brand' href='#'>Show Time: ${ctx.siteoptions.show_time}</a>
   </div>
  </div>
 </nav>
: end
