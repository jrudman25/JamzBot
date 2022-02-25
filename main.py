import discord
from discord.ext import commands
import os
from keep_running import keep_running
import music

# nix-env -iA nixpkgs.ffmpeg to install ffmpeg properly

client = commands.Bot(command_prefix = '^', intents = discord.Intents.all())
cogs = [music]

for i in range(len(cogs)):
  cogs[i].setup(client)

@client.event
async def on_ready():
  print('Successfully logged in!')
  await client.change_presence(activity=discord.Game(name="^support to get started!"))

keep_running()
client.run(os.environ.get('TOKEN'))
