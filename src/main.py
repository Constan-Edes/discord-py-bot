import json
import aiohttp
import discord
from config import *
from discord.ext import commands 
from requests import  Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from discord.ext.commands import has_permissions
from urllib import request, parse
from datetime import datetime
from re import findall
from time import sleep
from random import  choice


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', description='A bot for the Discord server', intents=intents, help_command=None)


# ============ CORE FUNCTIONS  ============ # 
# if the b bot is on,  print some info
@client.event
async def on_ready():
    print(f''' 
    Bot is online!
    {client.user.name}
    {client.user.id}
    {client.user.discriminator} 
    ---------------''')
    await client.change_presence(activity=discord.Game(name='!help'))


# print in console message from the user
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    date = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
    await client.process_commands(message)
    print(f'{message.author.name} {message.content} at {date}')
   
       

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

# create a embed with info abput one cryptocurrency
@client.command()
async def coin(ctx, coin):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
    
    parameters = {
        'slug': coin
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY, 
    }
    session = Session()
    session.headers.update(headers)
    try:
        data = session.get(url, params=parameters)
        data = json.loads(data.text)
        cmc_id = next(iter(data['data']))
        cmc_id = str(cmc_id)
        embed = discord.Embed(title=f'{data["data"][cmc_id]["name"]}', description=f'{data["data"][cmc_id]["description"]}', timestamp=datetime.utcnow(), color=discord.Color.blurple(), type='rich') 
        embed.set_thumbnail(url=f'{data["data"][cmc_id]["logo"]}')
        embed.add_field(name='Symbol', value=f'{data["data"][cmc_id]["symbol"]}')
        embed.add_field(name='Slug', value=f'{data["data"][cmc_id]["slug"]}')
        launched = data["data"][cmc_id]["date_launched"]
        launched = datetime.strptime(launched, '%Y-%m-%dT%H:%M:%S.%fZ')
        launched = launched.strftime('%d/%m/%Y')
        embed.add_field(name='Date Launched', value=f'{launched}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')

        embed.add_field(name="Explorer", value=f'{data["data"][cmc_id]["urls"]["explorer"][0]}')
        del data["data"][cmc_id]["urls"]["explorer"]

        for _,value in data['data'][cmc_id]['urls'].items():
            if value is not None and value != []:
                print(_, value)
                title = _.replace('_', ' ').capitalize()
                for url in value:
                    if 'discord' in url:
                        title = 'Discord'
                    if 't.me' in url:
                        title = 'Telegram'
                    
                    embed.add_field(name=f'{title}', value=f'{url}', inline=True)
        embed.set_footer(text=f'{ctx.me}', icon_url=f'{ctx.me.avatar_url}')
        embed.set_image(url=f'https://cdn.discordapp.com/attachments/959959092594634793/970322571256025088/ezgif.com-gif-maker_2.gif')
       
        await ctx.send(embed=embed)
    except (ValueError, KeyError, ConnectionError, Timeout, TooManyRedirects) as e:
        await ctx.send(f'{ctx.author.mention} There was an error with the request: {e}')
    

# show the price of the requested cryptocurrency 
@client.command()
async def price(ctx, currency:str='BTC', percentages:str='', fiat:str='USD'):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    currency = currency.upper()
    parameters = {
        'symbol': currency,
        'convert': fiat,
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    session = Session()
    session.headers.update(headers)
    try:
        fiats = {'USD', 'CHF', 'EUR', 'GBP', 'AUD', 'CAD', 'JPY', 'NZD', 'RUB', 'SEK', 'SGD', 'TRY', 'ZAR', 'BRL', 'CLP', 'CLY', 'ARS', 'MXN', 'KRW', 'TWD', 'UYU', 'TRY'}
        if fiat not in fiats:
            await ctx.send(f'{ctx.author.mention} The currency {fiat} is not supported!')
            return 
            
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        price = round(data['data'][currency][0]['quote'][fiat]['price'], 2)
        name = data['data'][currency][0]['name']
        percent_change_24h = round(data['data'][currency][0]['quote'][fiat]['percent_change_24h'], 1)
        percent_change_7d = round(data['data'][currency][0]['quote'][fiat]['percent_change_7d'], 2)
        percent_change_30d = round(data['data'][currency][0]['quote'][fiat]['percent_change_30d'], 2)
                
        result = f'{ctx.author.mention} The price of {name} is {price}  {fiat}.\n'

        if percentages == '-p' or percentages != '':
            result += f'\n{percent_change_24h}% in the last 24 hours.\
            \n{percent_change_7d}% in the last 7 days.\
            \n{percent_change_30d}% in the last 30 days.'

        await ctx.send(result)

    except (KeyError, TypeError, ValueError):
        return await ctx.send(f'{ctx.author.mention} The currency {currency} is not supported!')
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return await ctx.send(f'error: {e}')
        


@client.command()
async def say(ctx, *, msg):
    await ctx.channel.purge(limit=1)
    await ctx.send(msg)


# ============ MULTIMEDIA FUNCTIONS  ============ # 
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


# ============ MODERATION FUNCTIONS ============ # 
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

    
         