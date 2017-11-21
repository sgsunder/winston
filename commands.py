import asyncio

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
		
		if alias == None:
			name = func.__name__
		else:
			name = alias
		
		commands[name] = wrapper
		
		return wrapper
	return decorator

# --- commands --- #

# command example
@command()
async def rank(ctx):
	server_roles = ctx.server.roles
	roles = []
	
	for arg in ctx.args:
		for role in server_roles:
			if arg.upper() == role.name.upper():
				roles.append(role)
	
	await ctx.client.add_roles(ctx.author, *roles)
	await ctx.client.delete_message(ctx.message)