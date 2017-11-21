import discord
import asyncio
from settings import settings
from command_processor import CommandProcessor

client = discord.Client()
cp = CommandProcessor(client, settings.prefix)

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