import discord
from config import *
from discord.ext import commands 
from discord.ext.commands import has_permissions
from urllib import request, parse
from random import randint
from jokes import *
import datetime
import re

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', description='A bot for the Discord server', intents=intents, help_command=None)


# if the b bot is on, the bot print some info
@client.event
async def on_ready():
    print(f''' 
    {client.user.name}
    {client.user.id}
    {client.user.discriminator} 
    ---------------''')
    await client.change_presence(activity=discord.Game(name='!help'))

# send a message in the welcome channel when a new member join the server
@client.command()
async def on_member_join(ctx,member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    await channel.send(f'Welcome {member.mention} to {ctx.guild.name}! :mechanical_arm::smiling_imp:')

# send a message in to his autor when a member leave the server
@client.command()
async def on_member_remove(ctx,member):
    user = await client.fetch_user(AUTHOR_ID)
    await user.send(f'{member.mention} abandonded {ctx.guild.name}! :slight_frown:')

# send a message + the latency (for testings)
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# print info abput the actual server for users
@client.command()
async def info(ctx):
    embed = discord.Embed(title=f'{ctx.guild.name}', description='Discord server info', timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
    embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
    embed.add_field(name='Created At', value=f'{ctx.guild.created_at}')
    embed.add_field(name='Server Owner', value=f'{ctx.guild.owner}')
    embed.add_field(name='Server Region', value=f'{ctx.guild.region}')
    embed.add_field(name='Server ID', value=f'{ctx.guild.id}')
    embed.add_field(name='Your Server Role', value=f'{ctx.author.top_role}')
    embed.add_field(name='Server Members', value=f'{ctx.guild.member_count}')
    embed.set_footer(text=f'{ctx.me}', icon_url=f'{ctx.me.avatar_url}')
    embed.set_thumbnail(url=f'{ctx.guild.icon_url_as(format="png", size=1024)}')
    await ctx.send(embed=embed)

# send a joke to the chat from the DB
@client.command()
async def joke(ctx):
    selected = jokes[randint(0, len(jokes)-1)]
    print(selected)
    user = ctx.message.author.mention
    # punchline in bold :)
    await ctx.send(f'{user} Here is your joke: \n>>> {selected["joke"]}\n\n**{selected["punchline"]}**\n' )
    

# join the voice channel
@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send(f'You are not in a voice channel, you must be in one to use this command.')

# leave the voice channel
@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send(f'Invalid command.')

# search a youtube video
@client.command()
async def yt(ctx, *, search):
    author=ctx.message.author
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('watch\?v=(.{11})',html_content.read().decode('utf-8'))
    print(search_results)
    await ctx.send(f'{author.mention} Here is the search result:\n https://www.youtube.com/watch?v=' + search_results[0])

# play a song from youtube (FIX -------------------------------------------)
@client.command()
async def play(ctx, url):
    voice = await ctx.author.voice.channel.connect()
    #player = await youtube_dl.create_ytdl_player(url)
    #player.start()

# join the vc and play local songs (path = LOCAL_PATH)
@client.command()
async def plocal(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = discord.FFmpegPCMAudio(source=LOCAL_PATH)
        voice.play(source)
    else:
        await ctx.send(f'You are not in a voice channel, you must be in one to use this command.')

# pause the music 
@client.command(pass_context=True) 
async def ps(ctx):
    if ctx.voice_client:
        ctx.voice_client.pause()
    else:
        await ctx.send(f'Invalid command.')

# resume the music
@client.command(pass_context=True) 
async def rs(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        else:
            await ctx.send(f'Invalid command.')
    else:
        await ctx.send(f'Invalid command.')

# stop the music and leave the vc
@client.command(pass_context=True) 
async def st(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        ctx.voice_client.disconnect()
    else:
        await ctx.send(f'Invalid command.')

# skip the music
client.command()
async def skip(ctx):
    pass

# clear a number of messages in the chat
@client.command(pass_context=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages deleted.')

# kick a member from the server
client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

# ban a member from the server
@client.command(pass_context=True)
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


# functions in case of errors
# @kick.error
# async def kick_error(ctx, error):
#     if isinstance(error, commands.MissingPermissions):

#         await ctx.send(f'You don\'t have permissions to use this command.')
# @ban.error
# async def ban_error(ctx, error):
#     if isinstance(error, commands.MissingPermissions):

#         await ctx.send(f'You don\'t have permissions to use this command.')


# ======= END OF FILE ==============================================================================================

client.run(TOKEN)

    
         