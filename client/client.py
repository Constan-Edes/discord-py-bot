import os
from typing import List
from inspect import cleandoc
from discord import Game, Status, Intents
from discord.ext.commands import Bot
from core.config import settings, COGS_DIR
from cogwatch import watch


class CustomBot(Bot):
    def __init__(self, **options):
        super().__init__(
            command_prefix=settings.COMMAND_PREFIX,
            description=settings.DESCRIPTION,
            intents=Intents.all(),
            help_command=None,
            **options,
        )
        self.cogs_folder = COGS_DIR
        self.cogs_list = self.load_cogs(COGS_DIR)
    
    @watch(path='cogs', preload=True)
    async def on_ready(self):
        info = cleandoc(
            f"""\033[1m\033[92m
            Bot is online!
            Id: {self.user.id}
            Name: {self.user.name}
            Discriminator: {self.user.discriminator} 
            Description: {self.description}
            Prefix: {self.command_prefix}
            App Id: {self.application_id}
            Latency: {round(self.latency * 1000)}
            Creation Date: {self.user.created_at.date()}
            Cogs: {len(self.cogs)}
            Commands Synced: {len(self.all_commands)}
            Slash Commands Synced: {str(len(await self.tree.sync()))}
            ------------------------------------------------
            \033[0m"""
        )
        print(info)
        await self.change_presence(activity=Game(name='/help'), status=Status.online)
   
    async def setup_hook(self):
        await self.load_extension('jishaku')
        for cog in self.cogs_list:
            await self.load_extension(cog)

    def load_cogs(self, directory: str):
        cogs_list: List[str] = []
        for root, _, files in os.walk(directory):
            if "__pycache__" in root:
                continue
            folder_name = os.path.basename(root)
            for file_name in files:
                if file_name.endswith('.py'):
                    if folder_name == "cogs":
                        cogs_list.append(f"cogs.{file_name[:-3]}")
                    else:
                        cogs_list.append(f"cogs.{folder_name}.{file_name[:-3]}")
        return cogs_list
            



'''' async def info(ctx):
            embed = discord.Embed(
                title=f'{ctx.guild.name}',
                description='Discord server info',
                timestamp=datetime.utcnow(),
                color=discord.Color.green(),
            )
            embed.set_author(
                name=f'{ctx.author}', icon_url=f'{ctx.author.display_avatar}'
            )
            embed.add_field(name='Created At', value=f'{ctx.guild.created_at.date()}')
            embed.add_field(name='Server Owner', value=f'{ctx.guild.owner}')
            embed.add_field(name='Server Description', value=f'{ctx.guild.description}')
            embed.add_field(name='Server Members', value=f'{ctx.guild.member_count}')
            embed.add_field(name='Server ID', value=f'{ctx.guild.id}')
            embed.add_field(name='Your Server Role', value=f'{ctx.me.top_role}')
            embed.set_footer(text=f'{ctx.me}', icon_url=f'{ctx.me.display_avatar}')
            embed.set_thumbnail(url=f'{ctx.guild.icon}')
            await ctx.send(embed=embed)'
'''