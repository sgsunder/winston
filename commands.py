import asyncio
from settings import settings

commands = {}

# command decorator
# to create a new command, just make a function and put `@command()` on top of it
# parameters:
# 	alias: changes the name of the command
# 	pass_message: determines if the message should be passed to the function or not
def command(alias=None, pass_ctx=True):
	def decorator(func):
		async def wrapper(*args, **kwargs):
			try:
				if pass_ctx:
					await func(*args, **kwargs)
				else:
					await func()
			except Exception as e:
				print("Error in function ", func.__name__, ":\n", e)
		wrapper.__doc__  = func.__doc__
		
		if alias == None:
			name = func.__name__
		else:
			name = alias
		
		commands[name] = wrapper
		
		return wrapper
	return decorator

# --- commands --- #

@command()
async def help(ctx):
	"""Prints the docstring for a specific command"""
	docstring = commands[ctx.args[0]].__doc__
	
	if docstring == None:
		docstring = "No information provided"
	
	await ctx.client.send_message(ctx.channel, docstring)

@command()
async def rank(ctx):
	"""Gives or removes roles"""
	server_roles = ctx.server.roles
	user_roles = [ role.name for role in ctx.author.roles ]
	add_roles = []
	remove_roles = []
	
	for arg in ctx.args:
		for role in server_roles:
			if arg in settings.roles and arg == role.name:
				if arg in user_roles:
					remove_roles.append(role)
				add_roles.append(role)
				break
	
	await ctx.client.add_roles(ctx.author, *add_roles)
	await ctx.client.remove_roles(ctx.author, *remove_roles)
	await ctx.client.delete_message(ctx.message)
