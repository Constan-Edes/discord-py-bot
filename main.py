
import discord
from discord.ext import commands
from datetime import datetime
from os.path import isfile
from discord.ext.commands import Bot, DefaultHelpCommand
from decouple import config
import os
from rich import color


# Local imports
from src.cogs.entertaiment import EntertaimentCog
from src.cogs.finance import FinanceCog
from src.cogs.tools import ToolsCog
from src.cogs.moderation import ModerationCog
from src.cogs.multimedia import MultimediaCog





class BotClient(Bot):

    # if the bot is on, print some info
    async def on_ready(self):
        print(f'[green] Bot is online\n {self.user.name}\n{self.user.discriminator}')
        await self.change_presence(activity=discord.Game(name='!help', type=3))

    def __init__(self, command_prefix, help_command='!help', description=None, **options):
        super().__init__(
            command_prefix=command_prefix,
            help_command=help_command,
            description=description,
            **options
        )
        self.add_cog(EntertaimentCog(self))
        self.add_cog(ToolsCog(self))
        self.add_cog(FinanceCog(self))
        self.add_cog(ModerationCog(self))
        self.add_cog(MultimediaCog(self))

    # send a message in the welcome channel when a new member join the server
    async def on_member_join(self, ctx, member):
        channel = self.get_channel(config("WELCOME_CHANNEL_ID"))
        await channel.send(f'Welcome {member.mention} to {ctx.guild.name}! :mechanical_arm::smiling_imp:')

    # send a message in to his autor when a member leave the server

    async def on_member_remove(self, ctx, member):
        user = await self.fetch_user(config("AUTHOR_ID"))
        await user.send(f'{member.mention} abandonded {ctx.guild.name}! :slight_frown:')

    # on user message

    async def on_message(self, message):
        if message.author == self.user:
            return
        date = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        print(
            f'{message.author.name} said: {message.content} in {message.channel.name} at {date}')
        await self.process_commands(message)


def main():
        intents = discord.Intents.all()
        intents.members = True

        # Default properties
        COMMAND_PREFIX = config("COMMAND_PREFIX") or "!"
        DESCRIPTION = config("DESCRIPTION") or "Discord.py bot"
        COINMARKETCAP_API_KEY = config("COINMARKETCAP_API_KEY")
        AUTHOR_ID = config("AUTHOR_ID")
        WELCOME_CHANNEL_ID = config("WELCOME_CHANNEL_ID")
        LOCAL_PATH = config("LOCAL_PATH") or None
        TOKEN = config("TOKEN")


        HELP_COMMAND = DefaultHelpCommand(dm_help=True)
        HELP_COMMAND.sort_commands = True

        
        # CREATE THE BOT
        bot: BotClient = BotClient(command_prefix=COMMAND_PREFIX, help_command=HELP_COMMAND, description=DESCRIPTION)
        bot.run(TOKEN)



# ======= END OF FILE ==============================================================================================
if __name__ == '__main__':
    main()

    
         