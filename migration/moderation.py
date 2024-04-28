from discord import Member
from discord.app_commands import Range
from discord.ext.commands import  hybrid_command, has_permissions, Cog,  Context, MissingPermissions


class Moderation(Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    @hybrid_command(name="clear", description="Clear a number of messages from the chat")
    async def clear(ctx: Context, amount: Range[int, 1, 10] = 5):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} messages deleted.')

    # kick a member from the server
    @hybrid_command(name="kick", description="Kicks a user from the guild")
    @has_permissions(kick_members=True)
    async def kick(ctx: Context, member: Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')

    # ban a member from the server
    @commands.command(pass_context=True)
    @has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send('You don\'t have permissions to use this command.')

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send('You don\'t have permissions to use this command.')
