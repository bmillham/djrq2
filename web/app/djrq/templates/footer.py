# encoding: cinje

: from cinje.std.html import default_footer
: from datetime import datetime
: from web.core.release import colophon

: def site_footer styles=[], scripts=[]
    <center>
    <div class='container'>
     <div class='row'>
      <div class='col-md-12 center-block'>
       <b>
        &copy;2010-${datetime.now().year} Brian Millham
       </b>
       <a href='#' data-toggle='modal' data-target='#infoModal'>
        <span class='glyphicon glyphicon-info-sign' aria-hidden='true'></span>
       </a>
      </div>
     </div>
     <div class='row'>
      <div class='col-md-12 center-block'><i>This site is for informational purposes only. No music files are hosted or shared on this site</i></div>
     </div>
    </div>
    </center>
    : use default_footer styles=styles, scripts=scripts
: end
