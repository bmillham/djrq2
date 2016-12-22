# encoding: cinje

: from cinje.std.html import default_footer
: from datetime import datetime
: from web.core.release import colophon

: def site_footer styles=[], scripts=[]
    <center>
    <div class='container'>
     <div class='row'>
      <div class='col-md-4 center-block'><b>&copy;2010-${datetime.now().year} Brian Millham</b></div>
      <div class='col-md-4 center-block'>#{colophon}</div>
      <div class='col-md-4 center-block'><i>This site is for informational purposes only. No music files are hosted or shared on this site</i></div>
     </div>
     <div class='row'>
      <div class='col-md-4'><h5>Glyphicons courtesy of <a href='http://glyphicons.com'>glyphicons.com</a></h5></div>
      <div class='col-md-4'><h6>HTML/css/js Famework: <a href='http://getbootstrap.com'>Bootstrap</a></h6></div>
      <div class='col-md-4'><h6>Bootstrap Themes: <a href='http://bootswatch.com'>Bootswatch</a></h6></div>
     </div>
    </div>
    </center>
    : use default_footer styles=styles, scripts=scripts
: end
