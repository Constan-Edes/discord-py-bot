import discord
from requests import  Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from src.config import *
import datetime
import json


class Finances(discord.ext.commands.Cog, name = "Finances"):
    def __init__(self, bot):
        self.bot = bot

    # create a embed with info abput one cryptocurrency
    @bot.command()
    async def crypto(ctx, coin):
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
            
            try: 
                launched = data["data"][cmc_id]["date_launched"]
                launched = datetime.strptime(launched, '%Y-%m-%dT%H:%M:%S.%fZ')
                launched = launched.strftime('%d/%m/%Y')
                embed.add_field(name='Date Launched', value=f'{launched}')
                

            except (TypeError, KeyError):
                launched = 'Not available'
                embed.add_field(name='Date Launched', value=f'{launched}')
                

            embed.add_field(name="Explorer", value=f'{data["data"][cmc_id]["urls"]["explorer"][0]}')
            del data["data"][cmc_id]["urls"]["explorer"]

            embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
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
            price = str(round(data['data'][currency][0]['quote'][fiat]['price'], 2))
            if price[0] == "0":
                price =  round(data['data'][currency][0]['quote'][fiat]['price'], 6)
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
            

