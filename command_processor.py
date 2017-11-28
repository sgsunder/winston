import asyncio
from inspect import signature, Parameter
import traceback

from commands import Commands
from context import Context

class CommandError(Exception):
	pass

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
			m = message.content.lower().split(" ")
			command = m[0][len(self.prefix):]
			
			if command in self.commands:
				tmp = {
					"args": m[1:],
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
	#	check: a function that determines if the user is allowed to run a command
	#	delete_message: should the message be deleted
	def command(self, alias=None, check=None, delete_message=False):
		def decorator(func):
			async def wrapper(ctx):
				# function globals
				g = func.__globals__
				g["client"] = self.client
				g["commands"] = self.commands
				g["ctx"] = ctx
				g["command_help"] = self.command_help
				
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
					
					r = 0
					if check:
						if check(ctx):
							r = await func(*p)
						else:
							await self.client.send_message(ctx.channel, "You don't have permission to use this command")
					else:
						r = await func(*p)
					
					if r == -1:
						await self.client.send_message(ctx.channel, self.command_help(ctx.command, section="usage"))
					else:
						if delete_message:
							await self.client.delete_message(ctx.message)
						else:
							await self.client.add_reaction(ctx.message, u"\u2705")
				except Exception as e:
					await self.client.add_reaction(ctx.message, u"\u274E")
					print("Error in function ", func.__name__, ":\n", e, "\n", traceback.print_exc())
			
			wrapper.__doc__  = func.__doc__
			
			if alias == None:
				name = func.__name__
			else:
				name = alias
			
			self.commands[name] = wrapper
			
			return wrapper
		return decorator
	
	def command_help(self, command, section=None):
			if self.commands[command]:
				docstring = self.commands[command].__doc__
			else:
				return None
			
			if docstring == None:
				return None
			
			def process(docstring):
				docstring = docstring.replace("PREFIX!", self.prefix)
				lines = docstring.expandtabs().splitlines()
				
				if len(lines) == 1:
					return lines.rstrip()
				
				indent = 100
				for line in lines[1:]:
					stripped = line.lstrip()
					if stripped:
						indent = min(indent, len(line) - len(stripped))
				
				if section and "**" + section in docstring:
					sections = docstring.expandtabs().split("**")
					lines = []
					for s in sections:
						if s.upper().startswith(section.upper()):
							lst = s.splitlines()
							for l in lst:
								lines.append(l)
				
				trimmed = [ lines[0].strip() ]
				for line in lines[1:]:
					s = line[indent:].rstrip()
					
					if s.startswith("**"):
						s = s[2:]
					
					trimmed.append(s)
				return "```" + "\n".join(trimmed) + "```"
			return process(docstring)