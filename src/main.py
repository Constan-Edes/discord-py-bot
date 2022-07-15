
import discord
from discord.ext import commands
import asyncio
from client.custom_bot_client import *
from cogs.games import Games
from src.config import *

class MyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def load_extensions():
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                await bot.load_extension(f"cogs.{filename[:-3]}")

    async def main():
        async with MyBot(command_prefix=PREFIX) as bot:
            await bot.load_extensions()
            await bot.start('your_token')
    
    asyncio.run(main())
    


if __name__ == '__main__':
   
    bot = MyBot(command_prefix=COMMAND_PREFIX, description=DESCRIPTION, intents=discord.Intents.all())
    bot.add_cog(Games(bot))

    """ bot = MyBot(command_prefix=COMMAND_PREFIX, description=DESCRIPTION, intents=INTENTS)
    bot.run(TOKEN) """

   




"""




"""