# encoding: utf-8

class Admin:
    __dispatch__ = 'resource'
    __resource__ = 'admin'


    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context

    def get(self, *arg, **args):
        return "Admin pages not available. Please use the original sites <a href='http://{}.millham.net/admin'>admin</a> pages".format(self._ctx.djname)
