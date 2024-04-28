from inspect import cleandoc
import os
from discord import Game, Status, Intents
from discord.ext.commands import Bot
from datetime import datetime
from config import settings


class CustomBot(Bot):
    def __init__(self, **options):
        super().__init__(
            command_prefix=settings.COMMAND_PREFIX,
            description=settings.DESCRIPTION,
            intents=Intents.all(),
            help_command=None,
            **options,
        )
        self.cogs_folder = "./cogs"

    async def on_ready(self):
        info = cleandoc(
            f"""Bot is online!
            Description: {self.description}
            Latency: {self.latency}
            Prefix: {self.command_prefix}
            Creation Date: {self.user.created_at.date()}
            Owner Id: {self.owner_id}
            Application Id: {self.application_id}
            Cogs: {len(self.cogs)}
            Commands Synced: {len(self.all_commands)}
            Slash Commands Synced: {str(len(await self.tree.sync()))}
            Name: {self.user.name}
            Id: {self.user.id}
            Discriminator: {self.user.discriminator} 
            ---------------------------"""
        )
        print(info)
        await self.change_presence(activity=Game(name="/help"), status=Status.online)

    async def on_message(self, message):
        if message.author == self.user:
            return
        date = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        print(
            f"{message.author.name} said: {message.content} in {message.channel.name} at {date}"
        )
        await self.process_commands(message)

    async def on_member_join(self, member):
        channel = self.get_channel(settings.WELCOME_CHANNEL_ID)
        await channel.send(
            f"Welcome {member.mention} to {self.guild.name}! :mechanical_arm::smiling_imp:"
        )

    async def on_member_remove(self, member):
        user = await self.fetch_user(settings.AUTHOR_ID)
        await user.send(f"{member.mention} left {member.guild.name}! :slight_frown:")

    async def setup_hook(self):
        await self.load_extension("jishaku")
        for filename in os.listdir(self.cogs_folder):
            if filename.endswith(".py"):
                await self.load_extension(
                    f"{os.path.basename(self.cogs_folder)}.{filename[:-3]}"
                )


# TODO: implememnt custom help message
""" async def info(ctx):
            embed = discord.Embed(
                title=f"{ctx.guild.name}",
                description="Discord server info",
                timestamp=datetime.utcnow(),
                color=discord.Color.green(),
            )
            embed.set_author(
                name=f"{ctx.author}", icon_url=f"{ctx.author.display_avatar}"
            )
            embed.add_field(name="Created At", value=f"{ctx.guild.created_at.date()}")
            embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
            embed.add_field(name="Server Description", value=f"{ctx.guild.description}")
            embed.add_field(name="Server Members", value=f"{ctx.guild.member_count}")
            embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
            embed.add_field(name="Your Server Role", value=f"{ctx.me.top_role}")
            embed.set_footer(text=f"{ctx.me}", icon_url=f"{ctx.me.display_avatar}")
            embed.set_thumbnail(url=f"{ctx.guild.icon}")
            await ctx.send(embed=embed)"""
