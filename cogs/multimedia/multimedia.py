from core.cog_base import CogBase
from discord import Interaction, app_commands
from discord.ext.commands import Bot


class Multimedia(CogBase, name="Multimedia module", description="Multimedia reproduction module"):
    def __init__(self, bot: Bot):
        super().__init__(bot)

    @app_commands.command(name="join", description="Joins a voice channel")
    async def join(self, interaction: Interaction):
        vc = interaction.user.voice
        if vc is None:
            await interaction.response.send_message("You need to be in a voice channel to use this command!", ephemeral=True)
            return
        await vc.channel.connect()
        #await interaction.message.add_reaction(":white_check_mark:")
        

async def setup(bot: Bot) -> None:
    await Multimedia(bot).setup()
