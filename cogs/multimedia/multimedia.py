from core.cog_base import CogBase
from discord import Interaction, app_commands
from discord.ext.commands import Bot


class Multimedia(CogBase, name="Multimedia module", description="Multimedia reproduction module"):
    def __init__(self, bot: Bot):
        super().__init__(bot)

        """ self.channel_options = create_option(
            name="choice",
            description="You can only choose a VC!",
            option_type=SlashCommandOptionType.CHANNEL,
            required=True
        )
        only_vc_option['channel_types'] = [2]
        """
    @app_commands.command(name="join", description="Joins a voice channel")
    async def join(self, interaction: Interaction):
        vc = interaction.user.voice
        if vc is None:
            await interaction.response.send_message("You need to be in a voice channel to use this command!", ephemeral=True)
            return
        await vc.channel.connect()
        #await interaction.message.add_reaction(":white_check_mark:")



    """  @commands.hybrid_command(name="join")
    async def _connect(self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
      node = wavelink.NodePool.get_node()
      player = node.get_player(ctx.guild.id)
      try:
          channel = channel or ctx.author.channel.voice
      except AttributeError:
          return await ctx.send('No voice channel to connect to. Please either provide one or join one.')
      player: wavelink.Player = await channel.connect(cls=wavelink.Player)
      return player """
        

async def setup(bot: Bot) -> None:
    await Multimedia(bot).setup()
