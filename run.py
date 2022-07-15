#!/usr/bin/env python3

import json
import discord
from src.config import *
from discord.ext import commands 
from urllib import request, parse
from datetime import datetime
from time import sleep
from random import  choice


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='!', description='A bot for the discord server', intents=intents, help_command=None)

                                        
# if the b bot is on,  print some info
@client.event
async def on_ready():
    print(f'''Bot is online!
    {client.user.name}
    {client.user.id}
    {client.user.discriminator} 
    -------------------''')
    await client.change_presence(activity=discord.Game(name='!help'))


# print in console message from the user
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    date = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
    print(f'{message.author.name} said: {message.content} in {message.channel.name} at {date}')
    await client.process_commands(message)
       

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


# custom help command
@client.command()
async def help(ctx):
    print(f'{ctx.author.name} asked for help!')


# send a message + the latency (for testings)
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# print info abput the actual server for users
@client.command()
async def info(ctx):
    embed = discord.Embed(title=f'{ctx.guild.name}', description='Discord server info', timestamp=datetime.utcnow(), color=discord.Color.green())
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


# ============ ENTERTAINMENT FUNCTIONS  ============ # 
# send a joke to the chat from the DB
@client.command()
async def joke(ctx):
    user = ctx.message.author.mention
    url = 'https://jokes-api-py.herokuapp.com/api/jokes/random'
    res = request.urlopen(url).read()
    data = json.loads(res)
    await ctx.send(f'{user} Here is your joke: >>> {data["joke"]["joke"]}\n\n**{data["joke"]["punchline"]}**\n' )
    

# flip a coin
@client.command()
async def flip(ctx):
    user = ctx.message.author.mention
    await ctx.send(f'{user} The coin landed on...')
    sleep(1.4)
    await ctx.send(f'>>>{choice(["Heads!", "Tails!"])}')

# send a meme
@client.command()
async def meme(ctx):
    user = ctx.message.author.name
    url = 'https://meme-api.herokuapp.com/gimme'
    res = request.urlopen(url).read()
    data = json.loads(res)
    await ctx.send(data['url'])



@client.command()
async def say(ctx, *, msg):
    await ctx.channel.purge(limit=1)
    await ctx.send(msg)



client.run(TOKEN)

    
         