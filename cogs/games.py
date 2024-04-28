from discord.ext.commands import hybrid_command, Bot, Cog, Context

class Games(Cog, name="Games module"):
    def __init__(self, bot: Bot) -> Bot:
        self.bot = bot

    @hybrid_command(name="ping", description="For test purposes")
    async def ping(self, ctx: Context) -> None:
        await ctx.send(f"Pong! 🏓 {round(self.bot.latency * 1000)}ms")

    @hybrid_command(name="hello", description="Sends greeting")
    async def hello(self, ctx: Context) -> None:
        await ctx.send("Hello!")


async def setup(bot: Bot) -> None:
    await bot.add_cog(Games(bot))
