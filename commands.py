import asyncio

from settings import settings

class Commands:
	def __init__(self, decorator):
		command = decorator
		
		@command()
		async def help(command):
			"""Prints the docstring for a specific command"""
			if command != None:
				docstring = commands[command].__doc__
			else:
				docstring = "What command do you need help with?"
			
			if docstring == None:
				docstring = "No documentation available for this command"
			
			await client.send_message(ctx.channel, docstring)
		
		@command(delete_message=True)
		async def rank(role):
			"""Gives or removes roles"""
			server_roles = ctx.server.roles
			user_roles = [ role.name for role in ctx.author.roles ]
			
			for s_role in server_roles:
				if role in settings.roles and role == s_role.name:
					if role in user_roles:
						await client.remove_roles(ctx.author, s_role)
					else:
						await client.add_roles(ctx.author, s_role)