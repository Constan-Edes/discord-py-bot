from discord.ext.commands import Bot
from discord import Interaction, app_commands
from client.client import CustomBot
from core.checks import is_owner
from core.cog_base import CogBase


class Commands(CogBase, name="Commands module", description="Bot Commands"):
    def __init__(self, bot: CustomBot):
        super().__init__(bot)

    @app_commands.command(name="reload", description="Reloads a Cog Class")
    @app_commands.check(is_owner)
    async def reload(self, interaction: Interaction):
        try:
            for x in self.bot.cogs_list:
                await self.bot.reload_extension(x)
            await interaction.response.send_message("Successfully reloaded cogs")
        except Exception as e:
            await interaction.response.send_message(f"Failed! Could not reload cogs. See error below\n```{e}```")


async def setup(bot: Bot) -> None:
    await Commands(bot).setup()
