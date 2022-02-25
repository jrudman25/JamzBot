import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def support(self, ctx):
    await ctx.send("Use ^join to get the bot into the channel that you're in and ^play insertLinkHere to play. Use ^abilities for more!")

  @commands.command()
  async def updates(self, ctx):
    await ctx.send("Queue system, search capabilities, and (maybe) auto-deleting messages!")

  @commands.command()
  async def abilities(self, ctx):
    await ctx.send("^support, ^join, ^play, ^pause, ^resume, ^stop, ^disconnect, ^updates")
  
  @commands.command()
  async def join(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("You must be connected to a voice channel!")
    else:
      voice_channel = ctx.author.voice.channel
      if ctx.voice_client is None:
        await voice_channel.connect()
      else:
        await ctx.voice_client.move_to(voice_channel)
      
  @commands.command()
  async def play(self, ctx, url):
    if ctx.voice_client is None:
      await ctx.send("Must use join command before playing!")
      return
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':"bestaudio"}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      url2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
      vc.play(source)
      if ctx.voice_client.is_playing() is True:
        await ctx.send("Playing! :arrow_forward:")
      else:
        await ctx.send("Error! Please try another link :frowning:")

  @commands.command()
  async def stop(self, ctx):
    try:
      if ctx.voice_client.is_playing() is True:
        ctx.voice_client.stop()
        await ctx.send("Stopped! :x:")
      else:
        await ctx.send("Bot is not playing anything!")
    except AttributeError:
        await ctx.send("Bot is not playing anything!")

  @commands.command()
  async def disconnect(self, ctx):
    if ctx.voice_client is not None:
      await ctx.voice_client.disconnect()
      await ctx.send("Disconnected! :wave:")
    else:
      await ctx.send("Bot is not in a voice channel!")

  @commands.command()
  async def pause(self, ctx):
    try:
      if ctx.voice_client.is_playing() is True:
        ctx.voice_client.pause()
        await ctx.send("Paused! :pause_button:")
      else:
        await ctx.send("Bot is not playing anything!")
    except AttributeError:
        await ctx.send("Bot is not playing anything!")

  @commands.command()
  async def resume(self, ctx):
    try:
      if ctx.voice_client.is_playing() is True:
        await ctx.send("Bot is already playing something! :notes:")
        return
      
      ctx.voice_client.resume()
      if ctx.voice_client.is_playing() is True:
        await ctx.send("Resumed! :play_pause:")
      else:
        await ctx.send("Bot is not playing anything!")
    except AttributeError:
        await ctx.send("Bot is not playing anything!")

  @commands.Cog.listener()
  async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
          await ctx.send("Command unknown!")
          return
        else:
          await ctx.send("Something went wrong! Please try again")
      
# Setup
def setup(client):
  client.add_cog(music(client))
