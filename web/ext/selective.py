class SelectiveDefaultDatabase:
    needs = {'djdb'}
    provides = {'selective'}

    def __init__(self, fallback=None, **aliases):
        self.fallback = fallback
        self.aliases = aliases

    def prepare(self, context):
        host = self.aliases.get(context.djname, context.djname)
        if host not in context.db:
            if not self.fallback:
                return

            host = self.fallback

        context.db.__dict__['default'] = context.db[host]
