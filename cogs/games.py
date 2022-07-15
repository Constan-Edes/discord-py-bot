import discord
from discord.ext import commands

class Games(discord.ext.commands.Cog, name='Greetings module'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def pingg(self, ctx):
        await ctx.send('pong')

    
