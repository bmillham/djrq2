from .templates.notfound import notfound

class NotFound:
    __dispatch__ = 'resource'
    __resource__ = 'notfound'


    def __init__(self, context, name, *arg, **args):
        self._name = name
        self._ctx = context
        self._defaultdb = self._ctx.db.default
        self._db_model = A
        self._browsetemplate = browsetemplate

    def id(self, aid):
        try:
            a = self._ctx.db.default.query(A).filter(A.id == aid).one()
        except NoResultFound:
            return "ID not found"
        else:
            return "ID {}: {}".format(aid, a.fullname)

    def get(self, *arg, **args):
        if 'id' in args:
            return self.id(args['id'])
        else:
            return self.letters()

    def __call__(self, *arg, **args):
        print("call: ", arg, args)
