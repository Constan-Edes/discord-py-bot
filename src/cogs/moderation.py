from unicodedata import name
import discord
from discord.ext import commands 

class ModerationCog(commands.Cog, name='Moderation'):
    
    # pause the music 
    @commands.command(pass_context=True) 
    async def ps(ctx):
        if ctx.voice_client:
            ctx.voice_client.pause()
        else:
            await ctx.send(f'Invalid command.')

    # resume the music
    @commands.command(pass_context=True) 
    async def rs(ctx):
        if ctx.voice_client:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
            else:
                await ctx.send(f'Invalid command.')
        else:
            await ctx.send(f'Invalid command.')

    # stop the music and leave the vc
    @commands.command(pass_context=True) 
    async def st(ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            ctx.voice_client.disconnect()
        else:
            await ctx.send(f'Invalid command.')