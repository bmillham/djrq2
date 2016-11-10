# encoding: utf-8

__import__('cinje')

from web.core import Application
from web.ext.annotation import AnnotationExtension
from web.ext.debug import DebugExtension
from web.ext.serialize import SerializationExtension
from web.ext.djdb import DJDatabaseExtension
from web.ext.selective import SelectiveDefaultDatabase
from web.ext.dj import DJExtension
from web.ext.djhost import DJHostExtension
from .root import Root

app=Application(Root, extensions=[
		AnnotationExtension(),
		DebugExtension(),
		SerializationExtension(),
		DJDatabaseExtension(),
		SelectiveDefaultDatabase(),
		DJExtension(),
		DJHostExtension(),
		])

if __name__ == "__main__":
	app.serve('wsgiref', host='0.0.0.0')
