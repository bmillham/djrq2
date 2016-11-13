from ..templates.browse import browsetemplate

def letter(self, l):
    """ Returns artists/albums starting with selected letter """

    __dispatch__ = 'resource'

    self._ctx.selected_letter = l
    names = self._ctx.queries.get_names_by_letter(l)
    letterscountslist = self._ctx.queries.get_letters_counts()
    return browsetemplate("Browse by " + self._ctx.resource.__resource__.capitalize() + ": " + l, self._ctx, letterscountslist, names)
