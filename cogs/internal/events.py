from datetime import datetime
from core.config import settings
from discord import Member, Message
from discord.ext.commands import Bot, Cog
from core.cog_base import CogBase


class Events(CogBase, name="Events module", description="Handles the bot events"):
    def __init__(self, bot: Bot):
        super().__init__(bot)

    
    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author is self.bot.user:
            return
        date = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        print(
            f"{message.author.name} said: {message.content} in {message.channel.name} at {date}"
        )

    @Cog.listener()
    async def on_member_join(self, member: Member):
        channel = self.bot.get_channel(settings.WELCOME_CHANNEL_ID)
        await channel.send(
            f"Welcome {member.mention} to {self.guild.name}! :mechanical_arm::smiling_imp:"
        )

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        user = await self.bot.fetch_user(settings.AUTHOR_ID)
        await user.send(f"{member.name} left {member.guild.name}! :slight_frown:")
    

async def setup(bot: Bot) -> None:
    await Events(bot).setup()
