class SelectiveDefaultDatabase:
	needs = {'db'}
	
	def __init__(self, fallback=None, **aliases):
		self.fallback = fallback
		self.aliases = aliases
	
	def prepare(self, context):
		host = context.request.host.rpartition(":")[0].split('.')[0]
		host = self.aliases.get(host, host)
		if host not in context.db:
			if not self.fallback:
				return
			
			host = self.fallback
		
		context.db.__dict__['default'] = context.db[host]
		
