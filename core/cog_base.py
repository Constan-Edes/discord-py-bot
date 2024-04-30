from discord.ext.commands import Cog, CogMeta, Context, CommandError, Bot

class CogBase(Cog, metaclass=CogMeta):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot: Bot = bot

    async def cog_command_error(self, ctx: Context, error: CommandError):
        return await super().cog_command_error(ctx, error)


    async def cog_before_invoke(self, ctx: Context):
        return await super().cog_before_invoke(ctx)

    async def cog_after_invoke(self, ctx: Context):
        return await super().cog_after_invoke(ctx)

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__cog_name__} is online.")

    async def setup(self):
        await self.bot.add_cog(self)
