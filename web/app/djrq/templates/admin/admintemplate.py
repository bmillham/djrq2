# encoding: cinje

: from cinje.std.html import page as _page, default_header
: from ..footer import site_footer
: from .adminnavbar import adminnavbar

: default_styles = [
:           '/public/css/style.css',
:           '/public/css/jquery.fileupload.css',
:           '/public/css/jquery.fileupload-ui.css',
:           '/public/vertical-table.css',
:          ]
: scripts = ['https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js',
:            '/public/bootstrap/js/bootstrap.min.js',
:            '/public/js/eldarion-ajax.min.js',
:            '/public/js/NchanSubscriber.js',
:            '/public/js/request.js',
:            '/public/js/subscribe.js',
:            '/public/js/updatedatabase.js',
:           ]
: filescripts = ['/public/js/vendor/jquery.ui.widget.js',
:                '/public/js/jquery.iframe-transport.js',
:                '/public/js/jquery.fileupload.js',
:                '/public/js/jquery.fileupload-process.js',
:                '/public/js/tmpl.min.js',
:                '/public/js/load-image.all.min.js',
:                '/public/js/jquery.fileupload-image.js',
:                '/public/js/jquery.fileupload-audio.js',
:                '/public/js/jquery.fileupload-video.js',
:                '/public/js/jquery.fileupload-validate.js',
:                '/public/js/jquery.fileupload-ui.js',
:                '/public/js/main.js',
:               ]

: def page title, ctx, header=default_header, footer=site_footer, metadata=[], styles=[], scripts=scripts, **attributes
    : if ctx.resource.__resource__ == 'uploadfiles'
     : scripts = scripts + filescripts
    : end
    : if ctx.queries.is_updating()
     : scripts.append('/public/js/updatedatabasesubscribe.js')
    : end
    : styles = [ctx.themes[ctx.usertheme], ctx.fixes] + default_styles
    : title = 'Admin: ' + title
    : try
     : title = title + ' [{}]'.format(ctx.session.username) if ctx.session.authenticated else "Please Login"
    : except
     : title = title + ' Please Login'
    : end
    : using _page title, header=header, footer=footer, metadata=metadata, styles=styles, scripts=scripts, **attributes
        : use adminnavbar ctx
        <div id='main-content'>
        : yield
        </div>
    : end
: end
