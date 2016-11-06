# encoding: cinje

: from cinje.std.html import default_footer
: from datetime import datetime
: from web.core.release import colophon

: def site_footer styles=[], scripts=[]
	<center>
	 <h5>&copy;2010-${datetime.now().year} Brian Millham</h5>
	 <h5>Glyphicons courtesy of <a href='http://glyphicons.com'>glyphicons.com</a></h5>
	 #{colophon}
	 <h6>HTML/css/js Famework: <a href='http://getbootstrap.com'>Bootstrap</a></h6>
	 <h6>Bootstrap Themes: <a href='http://bootswatch.com'>Bootswatch</a></h6>
	 <h6><i>This site is for informational purposes only. No music files are hosted or shared on this site</i></h6>	 
	</center>
	: use default_footer styles=styles, scripts=scripts
: end
