from commands import commands
from context import Context

class CommandProcessor:
	def __init__(self, client, prefix):
		self.client = client
		self.prefix = prefix
		
	
	async def process_command(self, message):
		if message.content.startswith(self.prefix):
			m = message.content.split(" ")
			command = m[0][len(self.prefix):]
			
			if command in commands:
				tmp = {
					"args": m[1:],
					"client": self.client,
					"command": command,
					"message": message,
					"prefix": self.prefix
				}
				
				ctx = Context(**tmp)
				
				await commands[command](ctx)