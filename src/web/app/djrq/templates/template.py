# encoding: cinje

: from cinje.std.html import page as _page, default_header
: from .footer import site_footer
: from .mainnavbar import mainnavbar
: from .searchwindow import searchwindow
: from .requestwindow import requestmodal, mistagmodal

: styles = [
#:			'/public/bootstrap-3.3.7-dist/css/bootstrap.min.css',
:			'/public/bootstrap/css/united-bootstrap.min.css',
#:           '/public/bootstrap-3.3.7-dist/css/bootstrap-theme.min.css',
:			'/public/fix-padding.css',
:			'/public/vertical-navbar.css',
:		   ]
: scripts = ['https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js',
:            '/public/bootstrap/js/bootstrap.min.js',
:			 '/public/js/eldarion-ajax.min.js',
:			 '/public/js/request.js']

: def page title, ctx, header=default_header, footer=site_footer, metadata=[], styles=styles, scripts=scripts, **attributes
    : using _page title, header=header, footer=footer, metadata=metadata, styles=styles, scripts=scripts, **attributes
		: use searchwindow ctx
		: use requestmodal ctx
		: use mistagmodal ctx
        : use mainnavbar ctx
        <div id='main-content'>
        : yield
        </div>
    : end
: end
