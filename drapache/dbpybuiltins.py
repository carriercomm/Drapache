"""
Here are the functions that will ship with python executable code
"""

import dbapijinja
import sys
import signal
import time
	
def get_builtins(**kwargs):
	"""
	client is the client
	get_params are the params from the get request
	sandbox is the sandbox in which it runs
	"""
	
	client = kwargs['client']
	get_params = kwargs['get_params']
	sandbox = kwargs['sandbox']
	
	
	built_in_hash = {'GETPARAMS':get_params}
	def register(function):
	     
		curglobs = globals()
		curlocs = locals()
    
		def outer_wrapper(*args,**kwargs):

			for p in reversed(sandbox.protections):
				p.disable(sandbox)
			
			retval = function(*args,**kwargs)
			
			#redo the protections
			for p in sandbox.protections:
				p.enable(sandbox)
			
			return retval
		
		
		built_in_hash[function.func_name] = outer_wrapper
		return function
			
		
		
		
	@register
	def render_template(path,with_data=None,search_root="/_templates"):
		"""
		renders the given template
		"""
		
		print dbapijinja.render_dropbox_template(client,path,with_data,search_root)
		
	@register
	def die(message=""):
		"""
		Raises an Exception
		"""
		raise Exception(message)
		
		



		
		
		
		
		
	return built_in_hash
		
	