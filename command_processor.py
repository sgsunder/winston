import asyncio
from inspect import signature, Parameter

from commands import Commands
from context import Context

class CommandProcessor:
	def __init__(self, client, prefix):
		self.client = client
		self.commands = {}
		self.prefix = prefix
		
	def reload_commands(self, decorator):
		del self.commands
		self.commands = {}
		Commands(decorator)
	
	async def process_command(self, message):
		if message.content.startswith(self.prefix):
			m = message.content.split(" ")
			command = m[0][len(self.prefix):]
			
			if command in self.commands:
				
				
				tmp = {
					"args": m[1:],
					"client": self.client,
					"command": command,
					"message": message,
					"prefix": self.prefix
				}
				
				ctx = Context(**tmp)
				del tmp
				
				await self.commands[command](ctx)
	
	# command decorator
	# to create a new command, just make a function and put `@command()` on top of it
	# parameters:
	# 	alias: changes the name of the command
	#	delete_message: should the message be deleted
	def command(self, alias=None, delete_message=False):
		def decorator(func):
			async def wrapper(ctx, *args, **kwargs):
				# function globals
				g = func.__globals__
				g["client"] = self.client
				g["commands"] = self.commands
				g["ctx"] = ctx
				
				try:
					parameters = signature(func).parameters
					
					if len(parameters) > 0:
						positional = False
						for key in parameters:
							if parameters[key].kind == Parameter.VAR_POSITIONAL:
								positional = True
						
						if positional:
							p = ctx.args
						else:
							if len(ctx.args) >= len(parameters):
								p = ctx.args[:len(parameters)]
							else:
								p = ctx.args + [ None ] * (len(parameters) - len(ctx.args))
					else:
						p = []
						
					await func(*p)
					
					await self.client.add_reaction(ctx.message, u"\u2705")
				except Exception as e:
					await self.client.add_reaction(ctx.message, u"\u274E")
					print("Error in function ", func.__name__, ":\n", e)
				
				if delete_message:
					await self.client.delete_message(ctx.message)
			
			wrapper.__doc__  = func.__doc__
			
			if alias == None:
				name = func.__name__
			else:
				name = alias
			
			self.commands[name] = wrapper
			
			return wrapper
		return decorator