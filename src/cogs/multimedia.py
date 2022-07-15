import discord
from discord.ext import commands
from decouple import config

class MultimediaCog(commands.Cog, name='Multimedia'):
    # join the voice channel
    @commands.command(pass_context=True, name='join', help='Join the voice channel.')
    async def join(ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send(f'You are not in a voice channel, you must be in one to use this command.')

    # leave the voice channel
    @commands.command(pass_context=True)
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send(f'Invalid command.')

    # join the vc and play local songs (path = LOCAL_PATH)
    @commands.command()
    async def plocal(ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            source = discord.FFmpegPCMAudio(source=config('LOCAL_PATH'))
            voice.play(source)
        else:
            await ctx.send(f'You are not in a voice channel, you must be in one to use this command.')
