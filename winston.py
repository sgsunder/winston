import asyncio
import discord

from command_processor import CommandProcessor
from commands import Commands
from settings import settings

client = discord.Client()
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
	await cp.process_command(message)

client.run(settings.token)

try:
	loop.run_until_complete(client.login(settings.token))
	loop.run_until_complete(client.connect())
except KeyboardInterrupt:
	loop.run_until_complete(logout())
finally:
	loop.close()