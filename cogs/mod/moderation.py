from discord import Color, Embed, Interaction, Member
from core.cog_base import CogBase
from discord import app_commands
from discord.ext.commands import (
    Context,
    MissingPermissions,
    Bot,
    Range,
)

class Moderation(CogBase, name="Moderation", description="Guild moderation commands"):
    def __init__(self, bot: Bot):
        super().__init__(bot)

    @app_commands.command(
        name="clear", description="Clear a number of messages from the chat"
    )
    async def clear(ctx: Context, amount: Range[int, 1, 10] = 5):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"{amount} messages deleted.")

    # ban command
    @app_commands.command(name="ban", description="Bans a member.")
    @app_commands.describe(member="Member to ban.", reason="Reason to ban.")
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: Interaction, member: Member, reason: str = None):
        await member.ban(reason=reason)
        reason = "" if reason is None else f"\nReason: {reason}"
        ban_embed = Embed(
            title="🚫 ┃ Ban!",
            description=f"{member.mention} has been banned by {interaction.user.mention}{reason}",
            color=Color.red(),
        )
        await interaction.response.send_message(embed=ban_embed)
        await member.send(
            f"You have been banned from **{interaction.guild.name}**{reason}"
        )


    @app_commands.command(name="kick", description="Kicks a member.")
    @app_commands.describe(member="Member to kick.", reason="Reason to kick.")
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: Interaction,
        member: Member,
        reason: str = None,
    ):
        await member.kick(reason=reason)
        reason = "" if reason is None else f"\nReason: {reason}"
        kick_embed = Embed(
            title="🦵 ┃ Kick!",
            description=f"{member.mention} has been kicked by {interaction.user.mention}{reason}",
            color=Color.red(),
        )
        await interaction.response.send_message(embed=kick_embed)
        await member.send(
            f"You have been kicked from **{interaction.guild.name}**{reason}"
        )

    @kick.error
    async def kick_error(self, ctx: Context, error: Exception):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to use this command.")

    @ban.error
    async def ban_error(self, ctx: Context, error: Exception):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to use this command.")


async def setup(bot: Bot) -> None:
    await Moderation(bot).setup()
