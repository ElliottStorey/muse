import os
import discord
from discord.ext import commands
import youtube_dl
import asyncio
import requests
import random
import re
from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(
	command_prefix=['muse ', 'MUSE ', 'Muse '],
	case_insensitive=True,
  help_command=None,
  intents=intents
)

bot.author_id = 762704584435040286

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

async def errorm(ctx):
  embed=discord.Embed(title="Uh oh... An error occured. :sob:", color=0x18d7f3)
  embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
  embed.set_footer(text="Use muse add to invite Muse to your server!")
  await ctx.send(embed=embed)

async def adminm(ctx):
  embed=discord.Embed(title="Nice try... You need to be an admin to use this command.", color=0x18d7f3)
  embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
  embed.set_footer(text="Use muse add to invite Muse to your server!")
  await ctx.send(embed=embed)

@bot.event
async def on_ready():
  membercount = sum([g.member_count for g in bot.guilds])
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=f"to {membercount} users! Use muse help to view commands."))
  print(f"{bot.user} is online and listening to {membercount} users.")

@bot.event
async def on_member_join(member):
  for channel in member.guild.channels:
    if channel.name == 'new-members':
      embed=discord.Embed(title=f"Hi {member.name}! Welcome to {member.guild.name}!", color=0x18d7f3)
      embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
      embed.set_footer(text="Use muse help to view commands.")
      await channel.send(embed=embed)



@bot.command(aliases=['h'])
async def help(ctx, category=''):
  if category == '':
    embed=discord.Embed(title="Help", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.add_field(name="muse help", value="Displays this message.", inline=True)
    embed.add_field(name="muse help music", value="Displays music commands.", inline=True)
    embed.add_field(name="muse help fun", value="Displays fun commands.", inline=True)
    embed.add_field(name="muse help admin", value="Displays admin commands.", inline=True)
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)
  if category == 'music':
    embed=discord.Embed(title="Help music", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.add_field(name="muse help music", value="Displays this message.", inline=True)
    embed.add_field(name="muse play (song name)", value="Plays song in a vc.", inline=True)
    embed.add_field(name="muse join", value="Muse joins your current vc.", inline=True)
    embed.add_field(name="muse leave", value="Muse leaves its current vc.", inline=True)
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)
  if category == 'fun':
    embed=discord.Embed(title="Help fun", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.add_field(name="muse help fun", value="Displays this message.", inline=True)
    embed.add_field(name="muse meme", value="Displays a meme.", inline=True)
    embed.add_field(name="muse joke", value="Displays a joke.", inline=True)
    embed.add_field(name="muse insult (target)", value="Displays an insult.", inline=True)
    embed.add_field(name="muse say (message)", value="Muse repeats what you say.", inline=True)
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)
  if category == 'admin':
    embed=discord.Embed(title="Help admin", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.add_field(name="muse help admin", value="Displays this message.", inline=True)
    embed.add_field(name="muse kick (member)", value="Kicks the specified user.", inline=True)
    embed.add_field(name="muse ban (member)", value="Bans the specified user.", inline=True)
    embed.add_field(name="muse purge (amount)", value="Deletes specified amount of messages in a channel.", inline=True)
    embed.add_field(name="muse announce (message)", value="Sends embedded message in announcement channels.", inline=True)
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)

@bot.command()
async def add(ctx):
  embed=discord.Embed(title="Invite Link", color=0x18d7f3)
  embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
  embed.add_field(name="https://discord.com/api/oauth2/authorize?client_id=786314963542212628&permissions=8&scope=bot", value="\u200b", inline=True)
  embed.set_footer(text="DM Elliott Storey#1068 to suggest changes!")
  await ctx.send(embed=embed)

@bot.command(aliases=['p'])
async def play(ctx, *, url):
  try:
    for file in os.listdir():
      if 'youtube' in file:
        os.remove(file)
    await join(ctx)
    voice_channel = ctx.guild.voice_client
    async with ctx.typing():
      player = await YTDLSource.from_url(url, loop=bot.loop)
      voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    embed=discord.Embed(title="Now Playing", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.add_field(name=player.title, value="\u200b", inline=True)
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)
  except Exception as e:
    await errorm(ctx)
    print(e)

@bot.command(aliases=['j'])
async def join(ctx):
  try:
    await leave(ctx)
    channel = ctx.author.voice.channel
    await channel.connect()
  except Exception as e:
    await errorm(ctx)
    print(e)

@bot.command(aliases=['l', 'disconnect', 'stop'])
async def leave(ctx):
  try:
    voice_client = ctx.guild.voice_client
    if voice_client:
      await voice_client.disconnect()
  except Exception as e:
    await errorm(ctx)
    print(e)

@bot.command(aliases=['m'])
async def meme(ctx):
  try:
    queries = ['meme', 'memes', 'funnymeme', 'funnymemes', 'memer']
    num = random.randint(0, 4)
    r = requests.get(f'https://g.tenor.com/v1/search?key=85LY8DY0JV3Q&q={queries[num]}').json()
    results = r.get('results')
    num = random.randint(0, 19)
    results = results[num].get('media')
    results = results[0].get('gif')
    results = results.get('url')
    embed=discord.Embed(title="Meme", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.set_image(url=results)
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)
  except Exception as e:
    await errorm(ctx)
    print(e)

@bot.command(aliases=['funny'])
async def joke(ctx):
  r = requests.get(r'https://official-joke-api.appspot.com/random_joke')
  joke = r.json()
  embed=discord.Embed(title="Joke", color=0x18d7f3)
  embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
  embed.add_field(name=joke.get('setup'), value=joke.get('punchline'), inline=True)
  embed.set_footer(text="Use muse add to invite Muse to your server!")
  await ctx.send(embed=embed)


@bot.command(aliases=['i'])
async def insult(ctx, member: discord.Member=''):
  try:
    if member == '':
      member = ctx.author
    r = requests.get('https://insult.mattbas.org/api/insult')
    embed=discord.Embed(title=f"Insult for {member.name}", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.add_field(name=r.text, value="\u200b", inline=True)
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)
  except Exception as e:
    await errorm(ctx)
    print(e)

@bot.command(aliases=['s', 'repeat'])
async def say(ctx, *, message):
  try:
    message = re.sub('<.*?>', '', message)
    embed=discord.Embed(title="Say what?", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.add_field(name=message+'\u200b', value="\u200b", inline=True)
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)
  except Exception as e:
    await errorm(ctx)
    print(e)

@bot.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
  try:
    await bot.kick(member)
    embed=discord.Embed(title=f"{member} has been kicked.", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)
  except Exception as e:
    await errorm(ctx)
    print(e)

@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member):
  try:
    await bot.ban(member)
    embed=discord.Embed(title=f"{member} has been banned.", color=0x18d7f3)
    embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
    embed.set_footer(text="Use muse add to invite Muse to your server!")
    await ctx.send(embed=embed)
  except Exception as e:
    await errorm(ctx)
    print(e)

@bot.command(aliases=['clear', 'clean'])
@commands.has_permissions(administrator=True)
async def purge(ctx, limit : int):
  try:
    await ctx.channel.purge(limit=limit+1)
  except Exception as e:
    await errorm(ctx)
    print(e)

@bot.command(aliases=['a', 'announcement'])
@commands.has_permissions(administrator=True)
async def announce(ctx, *, message):
  try:
    for channel in ctx.guild.channels:
      if 'announce' in channel.name.lower():
        embed=discord.Embed(title="Announcement", color=0x18d7f3)
        embed.set_author(name="Muse", url="https://discordapp.com/users/786314963542212628/", icon_url="https://image.flaticon.com/icons/png/512/1534/1534491.png")
        embed.add_field(name=message, value="\u200b", inline=True)
        embed.set_footer(text="Use muse add to invite Muse to your server!")
        await channel.send(embed=embed)
  except Exception as e:
    await errorm(ctx)
    print(e)


keep_alive()
token = os.environ.get("TOKEN") 
bot.run(token)
