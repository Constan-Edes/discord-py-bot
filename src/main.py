import config
import discord
from datetime import datetime
from discord.ext import commands
from inspect import cleandoc



class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!', 
            intents=discord.Intents.all(),
            description="A bot for the discord server"
        )
        self.add_commands()

    async def on_ready(self):
        info = cleandoc(
            f'''Bot is online!
            {self.user.name}
            {self.user.id}
            {self.user.discriminator} 
            ---------------'''
        )
        print(info)
        await self.change_presence(activity=discord.Game(name='!help'), status=discord.Status.idle)
        
    async def on_message(self, message):
        await super().on_message(message)
        if message.author.name == self.user.name:
            return
        date = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        print(f'{message.author.name} said "{message.content}" at {date}')
        
    async def on_member_join(self, member):
        channel = self.get_channel(WELCOME_CHANNEL_ID)
        await channel.send(f'Welcome {member.mention} to {self.guild.name}! :mechanical_arm::smiling_imp:')
    
    async def on_member_remove(self, member):
        user = await self.fetch_user(AUTHOR_ID)
        await user.send(f'{member.mention} left {member.guild.name}! :slight_frown:')

    def add_commands(self):
        
        @self.command(name="ping", pass_context=True)
        async def ping(ctx):
            await ctx.send(f'Pong! {round(self.latency * 1000)}ms')
            
        @self.command(name="helpp", pass_context=True)
        async def help(ctx):
            print(f'{ctx.author.name} asked for help!')

        @self.command(name="info", pass_context=True)
        async def info(ctx):
            embed = discord.Embed(title=f'{ctx.guild.name}', description='Discord server info', timestamp=datetime.utcnow(), color=discord.Color.green())
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.display_avatar}')
            embed.add_field(name='Created At', value=f'{ctx.guild.created_at.date()}')
            embed.add_field(name='Server Owner', value=f'{ctx.guild.owner}')
            embed.add_field(name='Server Description', value=f'{ctx.guild.description}')
            embed.add_field(name='Server Members', value=f'{ctx.guild.member_count}')
            embed.add_field(name='Server ID', value=f'{ctx.guild.id}')
            embed.add_field(name='Your Server Role', value=f'{ctx.me.top_role}')
            embed.set_footer(text=f'{ctx.me}', icon_url=f'{ctx.me.display_avatar}')
            embed.set_thumbnail(url=f'{ctx.guild.icon}')
            await ctx.send(embed=embed)

def run() -> None:
    bot = BotClient()
    bot.run(DISCORD_TOKEN, root_logger=True)


if __name__ == "__main__":
    run()
