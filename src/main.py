import discord
from config import *
from discord.ext import commands 
from urllib import request, parse
from random import randint
import datetime
import sqlite3
import re

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', description='A bot for the Discord server', intents=intents)

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
    await user.send(f'{member.mention} abandono {ctx.guild.name}! :slight_frown:')


# send a message + the latency for testings
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# print info abput the actual server for users
@client.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description='Discord server info', timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    embed.add_field(name="Created At", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.add_field(name="Your Server Role", value=f"{ctx.author.top_role}")
    embed.add_field(name="Server Members", value=f"{ctx.guild.member_count}")
    embed.set_footer(text=f"{ctx.me}", icon_url=f"{ctx.me.avatar_url}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url_as(format='png', size=1024)}")
    await ctx.send(embed=embed)


# send a joke to the chat from the DB
@client.command()
async def joke(ctx):
    query = 'SELECT * FROM bad_jokes_short'
    conn = sqlite3.connect('jokes.db') 
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    selected = result[randint(0, len(result))] 
    user = ctx.message.author.mention
    # if the joke no have punchline
    if selected[2] == 0:
        await ctx.send(f"{user} aca tenes tu chiste: \n\n>>> **{selected[1]}**" )
    # punchline in bold :)
    await ctx.send(f"{user} aca tenes tu chiste: \n>>> {selected[1]}\n\n**{selected[2]}**\n" )
    conn.close()


# join the voice channel
@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel, you must be in one to use this command.")


# leave the voice channel
@client.command(pass_context=True)
async def leave(ctx):

    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Invalid command.")


# join the vc and play local music (path = LOCAL_PATH)
@client.command()
async def plocal(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
    else:
        player = voice.play(discord.FFmpegPCMAudio(source=LOCAL_PATH))
        await ctx.send("You are not in a voice channel, you must be in one to use this command.")






# ======= END OF FILE ==============================================================================================

# @client.command()
# async def yt(ctx, *, url):
#     query_string = parse.urlencode('search_query', url)
#     html_content = request.urlopen(f'https://www.youtube.com/results?{query_string}')
#     re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
#     await ctx.send(f'https://www.youtube.com/watch?v=')

client.run(TOKEN)

    
         