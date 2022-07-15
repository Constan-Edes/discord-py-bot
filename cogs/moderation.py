import discord
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands


class Moderation(discord.ext.commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    # ============ MODERATION FUNCTIONS ============ # 
    # clear a number of messages in the chat
    @client.command(pass_context=True)
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} messages deleted.')

    # kick a member from the server
    client.command()
    @has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')

    # ban a member from the server
    @client.command(pass_context=True)
    @has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')


    # functions in case of errors
    # @kick.error
    # async def kick_error(ctx, error):
    #     if isinstance(error, commands.MissingPermissions):

    #         await ctx.send(f'You don\'t have permissions to use this command.')
    # @ban.error
    # async def ban_error(ctx, error):
    #     if isinstance(error, commands.MissingPermissions):

    #         await ctx.send(f'You don\'t have permissions to use this command.')


    # ======= END OF FILE ==============================================================================================