from distutils.command.config import config
import json
import discord
from requests import Session
from datetime import datetime
from discord.ext import commands

class FinanceCog(commands.Cog, name='Finance'):
    def __init__(self, bot):
        self.bot = bot

    # create a embed with info abput one cryptocurrency
    @commands.command(name='coin', help='Get info about a cryptocurrency')
    async def coin(ctx, coin):
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
        parameters = {'slug': coin}
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': config("COINMARKETCAP_API_KEY")}
        session = Session()
        session.headers.update(headers)
        try: 
            data = session.get(url, params=parameters)
            data = json.loads(data.text)
            cmc_id = next(iter(data['data']))
            cmc_id = str(cmc_id)
        except Exception as e:
            await ctx.send(f'{ctx.author.mention} There was an error with the request: {e}')

        embed = discord.Embed(title=f"{data['data'][cmc_id]['name']}", description=f"{data['data'][cmc_id]['description']}", timestamp=datetime.utcnow(), color=discord.Color.blurple(), type='rich') 
        embed.set_thumbnail(url=f"{data['data'][cmc_id]['logo']}")
        embed.add_field(name='Symbol', value=f"{data['data'][cmc_id]['symbol']}") 
        embed.add_field(name='Slug', value=f"{data['data'][cmc_id]['slug']}") 
        embed.add_field(name='Date Launched', value=f"{data['data'][cmc_id]['date_launched'].stptime('%Y-%m-%dT%H:%M:%S.%fZ', '%d/%m/%Y') or 'N/A'}")
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.add_field(name='Explorer', value=f"{data['data'][cmc_id]['urls']['explorer'][0] or 'N/A'}")
        embed.add_field(name='Website', value=f"{data['data'][cmc_id]['links']['website'][0] or 'N/A'}")

        for _,value in data['data'][cmc_id]['urls'].items():
            embed.add_field(name=_, value=f'{value[0]}')

        embed.set_footer(text=f'{ctx.me}', icon_url=f'{ctx.me.avatar_url}')
        embed.set_image(url=f'https://cdn.discordapp.com/attachments/959959092594634793/970322571256025088/ezgif.com-gif-maker_2.gif')
        await ctx.send(embed=embed)
        

    # show the price of the requested cryptocurrency
    @commands.command(name='price', help='Get the price of a cryptocurrency')
    async def price(ctx, currency:str='BTC', percentages:str='', fiat:str='USD'):
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        currency = currency.upper()
        parameters = {'symbol': currency,'convert': fiat}
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': config("COINMARKETCAP_API_KEY")}
        session = Session()
        session.headers.update(headers)
    
        fiats = {'USD', 'CHF', 'EUR', 'GBP', 'AUD', 'CAD', 'JPY', 'NZD', 'RUB', 'SEK', 'SGD', 'TRY', 'ZAR', 'BRL', 'CLP', 'CLY', 'ARS', 'MXN', 'KRW', 'TWD', 'UYU', 'TRY'}
        if fiat not in fiats:
            await ctx.send(f'{ctx.author.mention} The fiat currency {fiat} is not supported.')
            return
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        price = round(data['data'][currency][0]['quote'][fiat]['price'], 2)
        name = data['data'][currency][0]['name']
        percent_change_24h = round(data['data'][currency][0]['quote'][fiat]['percent_change_24h'], 1)
        percent_change_7d = round(data['data'][currency][0]['quote'][fiat]['percent_change_7d'], 2)
        percent_change_30d = round(data['data'][currency][0]['quote'][fiat]['percent_change_30d'], 2)
        result = f'{ctx.author.mention} The price of {name} is {price}  {fiat}.'

        if percentages == '-p' or percentages != '':
            result += f'\n{percent_change_24h}% in the last 24 hours.\
            \n{percent_change_7d}% in the last 7 days.\
            \n{percent_change_30d}% in the last 30 days.'
                
        await ctx.send(result)

        