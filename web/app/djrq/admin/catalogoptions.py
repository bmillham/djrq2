# encoding: utf-8

from ..templates.admin.catalogoptions import catalogoptionstemplate

class CatalogOptions:
    __dispatch__ = 'resource'
    __resource__ = 'catalogoptions'

    def __init__(self, context, name, *arg, **args):
        self._ctx = context
        self.queries = context.queries
        self.cats = self.queries.get_catalogs()

    def get(self, *arg, **args):
       return catalogoptionstemplate("Catalog Selection", self._ctx, cats=self.cats)

    def post(self, *arg, **args):
        result = self.queries.save_siteoptions(**args)
        return catalogoptionstemplate("Catalog Selection Saved", self._ctx, cats=self.cats, saved=True)
