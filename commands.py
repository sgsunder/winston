import asyncio

import permissions
from settings import settings

class Commands:
	def __init__(self, decorator):
		command = decorator
		
		@command()
		async def help(command, section=None):
			"""Prints the docstring for a specific command
			
			**Usage:
				PREFIX!help <command>"""
			if command in commands:
				docstring = command_help(command, section)
			else:
				docstring = "What command do you need help with?"
			
			if docstring == None:
				docstring = "No documentation available for this command"
			
			await client.send_message(ctx.channel, docstring)
		
		@command(delete_message=True)
		async def rank(role):
			"""Gives or removes roles
			
			**Usage:
				PREFIX!rank <role>"""
			server_roles = ctx.server.roles
			user_roles = [ role.name for role in ctx.author.roles ]
			
			for s_role in server_roles:
				if role in settings.roles and role == s_role.name:
					if role in user_roles:
						await client.remove_roles(ctx.author, s_role)
					else:
						await client.add_roles(ctx.author, s_role)
		
		@command(check=permissions.is_mod, delete_message=True)
		async def purge(arg1, arg2=None): # can be int and None or mention and int
			"""Deletes messages
			
			**Usage:
				PREFIX!purge <num>
				or
				PREFIX!purge <@mention> <num>"""
			def get_int(n):
				try:
					return int(n)
				except ValueError:
					return -1
			
			m = None
			if arg2 == None:
				n = get_int(arg1)
			else:
				n = get_int(arg2)
				mentions = ctx.message.mentions
				for member in mentions:
					if member.mention == arg1:
						m = member
			
			if n == -1 or (arg2 != None and m == None):
				return -1
			
			def check(message):
				print(message.content)
				if arg2 == None:
					return True
				
				if message.author == m:
					return True
			
			to_delete = []
			tries_left = 5
			tmp = ctx.message
			while tries_left and len(to_delete) - 1 < n:
				async for message in client.logs_from(ctx.channel, limit=100, before=tmp):
					if len(to_delete) - 1 < n and check(message):
						to_delete.append(message)
					tmp = message
				tries_left -= 1
			
			await client.delete_messages(to_delete)