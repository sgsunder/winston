import discord
import asyncio
from commands import say
from commands import commands

client = discord.Client()
token = "MzgyNTYzNDk0OTIwMTkyMDEx.DPXhng.qa786qE11E9B2jXD46Pum9k7kOk"
prefix = "w!"

@client.event
async def on_ready():
  print("Logged in as")
  print(client.user.name)
  print(client.user.id)
  print("------")

@client.event
async def on_message(message):
	await process_command(message)
	

async def process_command(message):
	if message.content.startswith(prefix):
		m = message.content.split(" ")
		command = m[0][len(prefix):]
		
		if command in commands:
			await commands[command](message)


client.run(token)