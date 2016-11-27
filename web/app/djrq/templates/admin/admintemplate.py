# encoding: cinje

: from cinje.std.html import page as _page, default_header
: from ..footer import site_footer
: from .adminnavbar import adminnavbar

: default_styles = [
:           '/public/fix-padding.css',
:           '/public/vertical-table.css',
:          ]
: scripts = ['https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js',
:            '/public/bootstrap/js/bootstrap.min.js',
:            '/public/js/eldarion-ajax.min.js',
:            '/public/js/NchanSubscriber.js',
:            '/public/js/request.js',
:            '/public/js/subscribe.js',
:           ]

: def page title, ctx, header=default_header, footer=site_footer, metadata=[], styles=[], scripts=scripts, **attributes
    : styles = [ctx.themes[ctx.usertheme], ctx.fixes] + default_styles
    : title = 'Admin: ' + title
    : title = title + ' [{}]'.format(ctx.session.username) if ctx.session.authenticated else "Please Login"
    : using _page title, header=header, footer=footer, metadata=metadata, styles=styles, scripts=scripts, **attributes
        : use adminnavbar ctx
        <div id='main-content'>
        : yield
        </div>
    : end
: end
