import discord
from discord.ext import commands


class ToolsCog(commands.Cog, name='Tools'):
    def __init__(self, bot):
        self.bot = bot

    
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} messages deleted.')