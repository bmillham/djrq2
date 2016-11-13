# encoding: cinje

: from .template import page

: def notfound ctx, nfpage
    : using page "Not Found", ctx, lang="en"
        <h1>Page not found: ${nfpage}</h1>
        : yield
    : end
: end
