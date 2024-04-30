import discord 
from re import findall
from urllib import request, parse


class Multimedia(discord.ext.commands.Cog, name="Multimedia"):
    def __init__(self, bot):
        self.bot = bot

    # ============ MULTIMEDIA FUNCTIONS  ============ # 
    # join the voice channel
    

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
        search_results = findall('watch\?v=(.{11})',html_content.read().decode('utf-8'))
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
