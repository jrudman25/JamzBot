import discord
from discord.ext import commands
import os
from keep_running import keep_running
import music

client = commands.Bot(command_prefix = '^', intents = discord.Intents.all())
clientName = discord.Client()
cogs = [music]

for i in range(len(cogs)):
  cogs[i].setup(client)

@client.event
async def on_ready():
  print('Successfully logged in as {0.user}'.format(clientName))
  await client.change_presence(activity=discord.Game(name="^support to get started!"))

keep_running()
client.run(os.environ.get('TOKEN'))
