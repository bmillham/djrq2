from ..templates.browse import browsetemplate

def letters(self):
	""" Returns first letter of artists/albums, with count """
	lclist = self._ctx.queries.get_letters_counts()
	return browsetemplate("Browse by " + self._ctx.resource.__resource__.capitalize(), self._ctx, lclist)

