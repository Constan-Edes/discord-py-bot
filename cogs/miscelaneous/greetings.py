from discord.ext.commands import Bot
from discord import Interaction, app_commands
from core.cog_base import CogBase


class Greetings(CogBase, name="Greetings module", description="Bot presentations for testing purposes"):
    def __init__(self, bot: Bot):
        super().__init__(bot)

    @app_commands.command(name="ping", description="For test purposes")
    async def ping(self, interaction: Interaction) -> None:
        await interaction.response.send_message(f"Pong!🏓 {round(self.bot.latency * 1000)}ms")


    @app_commands.command(name="hello", description="Sends greeting")
    async def hello(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello!")

    
    @app_commands.command(name="hi", description="Sends greeting")
    async def hi(self, interaction: Interaction) -> None:
        await interaction.response.send_message("hi!")

async def setup(bot: Bot) -> None:
    await Greetings(bot).setup()
