class DJHostExtension:
	""" Parse the host name to find the DJ name, and save info that
		will be used in various places """
	first = True # Parse the host name before anything else is done
	provides = {'djhost'}
	
	def __init__(self, **args):
		pass
	
	def prepare(self, context):
		host, sep, host_domain = context.request.host.partition('.')
		if '-' in host: # So we can handle dj-name and name
			prefix, host = host.split('-')
		else:
			prefix = ''
		
		context.__dict__['host_domain'] = host_domain
		context.__dict__['djname'] = host
		context.__dict__['djprefix'] = prefix
		context.__dict__['djhost'] = sep.join((host, host_domain))
