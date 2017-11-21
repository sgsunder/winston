import asyncio

commands = {}

#
# to create a new command, just make a function and put `@command()` on top of it
# parameters:
# 	alias: changes the name of the command
# 	pass_message: determines if the message should be passed to the function or not
#

def command(alias=None, pass_message=True):
	def decorator(func):
		async def wrapper(*args, **kwargs):
			try:
				if pass_message:
					await func(*args, **kwargs)
				else:
					await func()
			except Exception as e:
				print(e)
		
		if alias == None:
			name = func.__name__
		else:
			name = alias
		
		commands[name] = wrapper
		
		return wrapper
	return decorator

# small example
@command()
async def say(message):
	print(message.content)
