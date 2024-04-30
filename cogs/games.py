from discord.ext.commands import Bot
from core.cog_base import CogBase


class Games(CogBase, name="Games module", description="Bot games"):
    def __init__(self, bot: Bot):
        super().__init__(bot)

async def setup(bot: Bot) -> None:
    await Games(bot).setup()
