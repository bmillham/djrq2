class SelectiveDefaultDatabase:
	needs = {'db'}
	
	def __init__(self, fallback=None, **aliases):
		self.fallback = fallback
		self.aliases = aliases
	
	def prepare(self, context):
		host, sep, host_domain = context.request.host.partition('.')
		if '-' in host: # So we can handle dj-name and name
			prefix, host = host.split('-')
		else:
			prefix = ''
		host = self.aliases.get(host, host)
		if host not in context.db:
			if not self.fallback:
				return
			
			host = self.fallback
		
		context.db.__dict__['default'] = context.db[host]
		context.__dict__['host_domain'] = host_domain
		context.__dict__['djname'] = host
		context.__dict__['djprefix'] = prefix
		context.__dict__['djhost'] = sep.join((host, host_domain))
