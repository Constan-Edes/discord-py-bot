import json
import random
import discord
from time import sleep
from discord.ext import commands
from datetime import datetime
from requests import request 

# ============ ENTERTAINMENT FUNCTIONS  ============ # 
class EntertaimentCog(commands.Cog, name='Entertaiment'):
    def __init__(self, bot):
        self.bot = bot

    # send a message + the latency (for testings)
    @commands.command(name='ping', help='Ping')
    async def ping(self, ctx):
        await ctx.send(f'Pong! :ping_pong: {round(self.bot.latency * 1000)}ms')


    # send a meme
    @commands.command(name='meme', help='Send a meme')
    async def meme(ctx):
        user = ctx.message.author.name
        url = 'https://meme-api.herokuapp.com/gimme'
        res = await request.urlopen(url).read()
        data = json.loads(res)
        await ctx.send(f'{user} here is your meme: {data["url"]}')


    # send a random cat
    @commands.command(name='cat', help='Send a random cat')
    async def cat(ctx):
        user = ctx.message.author.name
        url = 'https://aws.random.cat/meow'
        res = await request.urlopen(url).read()
        data = json.loads(res)
        await ctx.send(f'{user} here is your cat: {data["file"]}')


    @commands.command(name='dog', help='Send a random dog')
    async def dog(ctx):
        user = ctx.message.author.name
        url = 'https://random.dog/woof.json'
        res = await request.urlopen(url).read()
        data = json.loads(res)
        await ctx.send(f'{user} here is your dog: {data["url"]}')


    @commands.command(name='whoami', help='Who am i?')
    async def whoami(ctx):
        await ctx.send(f"""{ctx.author.mention} I\'m a bot created by Constantino Edes.
        You can find me on GitHub: https://github.com/constanedes\n\n or Discord: Constan#0909""")
        

    # print info abput the actual server for users
    @commands.command(name='serverinfo', help='Print info about the server and user')
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

    # send a joke to the chat from the DB
    @commands.command(name='joke', help='Send a random joke')
    async def joke(ctx):
        user = ctx.message.author.mention
        url = 'https://jokes-api-py.herokuapp.com/api/jokes/random'
        res = request.urlopen(url).read()
        data = json.loads(res)
        await ctx.send(f'{user} Here is your joke: >>>\n {data["joke"]["joke"]}\n\n**{data["joke"]["punchline"]}**\n' )
        

    # flip a coin
    @commands.command(name='flip', help='Flip a coin')
    async def flip(ctx):
        await ctx.send(f'The coin landed on... ')
        sleep(1.2)
        await ctx.send(f'>>>{random.choice(["Heads!", "Tails!"])} :coin:')

    # say something
    @commands.command(name='say', help='Say something')
    async def say(ctx, *, msg):
        await ctx.channel.purge(limit=1)
        await ctx.send(msg)

    # send a random number
    @commands.command(name='random', help='Send a random number')
    async def random(ctx, min = 1, max = 100) -> int:
        await ctx.send(f'{random.randint(min, max)}')


    # roll a dice
    @commands.command( name='roll', help='Roll a dice')
    async def dice(ctx):
        await ctx.send(f'{random.randint(1, 6)}')
        