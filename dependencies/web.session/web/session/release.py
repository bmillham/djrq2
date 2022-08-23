# encoding: utf-8

"""Release information about WebCore Sessions."""

# ## Imports

from __future__ import unicode_literals

import sys
from collections import namedtuple


# ## Module Globals

version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))(2, 0, 0, 'final', 0)
version = ".".join([str(i) for i in version_info[:3]]) + ((version_info.releaselevel[0] + str(version_info.serial)) if version_info.releaselevel != 'final' else '')

author = namedtuple('Author', ['name', 'email'])("Alice Bevan-McGregor", 'alice@gothcandy.com')
description = "Generalized session abstraction and basic engines for the WebCore web framework."
copyright = "2009-2016, Alice Bevan-McGregor and contributors"
url = 'https://github.com/marrow/web.session/'

