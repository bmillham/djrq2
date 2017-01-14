# encoding: cinje

: from cinje.std.html import page as _page, default_header
: from .footer import site_footer
: from .mainnavbar import mainnavbar
: from .bottomnavbar import bottomnavbar
: from .searchwindow import searchwindow
: from .requestwindow import requestmodal, mistagmodal, suggestionmodal, infomodal
: import os

: default_styles = [
:           '/public/vertical-navbar.css',
:           '/public/css/bootstrap-sortable.css',
:          ]
: scripts = ['https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js',
:            '/public/bootstrap/js/bootstrap.min.js',
:            '/public/js/eldarion-ajax.min.js',
:            '/public/js/NchanSubscriber.js',
:            '/public/js/request.js',
:            '/public/js/subscribe.js',
:            '/public/js/enable_tooltips.js',
:            '/public/js/bootstrap-sortable.js',
:           ]

: def page title, ctx, header=default_header, footer=site_footer, metadata=[], styles=[], scripts=scripts, **attributes
    : styles = [ctx.themes[ctx.usertheme], ctx.fixes]
    : styles = styles + default_styles
    : if ctx.siteoptions.show_title != '' and ctx.siteoptions.show_time != ''
     : styles.append(ctx.bfixes) # Add styles needed for the bottom navbar
    : end

    : using _page title, header=header, footer=footer, metadata=metadata, styles=styles, scripts=scripts, **attributes
        : use searchwindow ctx
        : use requestmodal ctx
        : use mistagmodal ctx
        : use suggestionmodal ctx
        : use infomodal ctx
        : use mainnavbar ctx
        <div id='main-content'>
        : yield
        </div>
        : if ctx.siteoptions.show_title != '' and ctx.siteoptions.show_time != ''
         : use bottomnavbar ctx
        : end
    : end
: end
