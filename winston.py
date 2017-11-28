import asyncio
import discord

from command_processor import CommandProcessor
from commands import Commands
from settings import settings

loop = asyncio.get_event_loop()
client = discord.Client(loop=loop)
cp = CommandProcessor(client, settings.prefix)
cp.reload_commands(cp.command)

@client.event
async def on_ready():
	print("Logged in as")
	print(client.user.name)
	print(client.user.id)
	print("------")

@client.event
async def on_message(message):
	# TODO: handle moderation thing
	await cp.process_command(message)

try:
	loop.run_until_complete(client.login(settings.token))
	loop.run_until_complete(client.connect())
except Exception as e:
	print(e)
	loop.run_until_complete(logout())
finally:
	loop.close()