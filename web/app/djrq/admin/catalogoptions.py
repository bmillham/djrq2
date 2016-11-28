# encoding: utf-8

from ..templates.admin.catalogoptions import catalogoptionstemplate

class CatalogOptions:
    __dispatch__ = 'resource'
    __resource__ = 'catalogtoptions'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries
        self.cats = self.queries.get_catalogs()

    def get(self, *arg, **args):
       so = self.queries.get_siteoptions()
       return catalogoptionstemplate("Catalog Selection", self._ctx,  siteoptions=so, cats=self.cats)

    def post(self, *arg, **args):
        result = self.queries.save_siteoptions(**args)
        so = self.queries.get_siteoptions()
        return catalogoptionstemplate("Catalog Selection Saved", self._ctx,  siteoptions=so, cats=self.cats, saved=True)
