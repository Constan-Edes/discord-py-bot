from discord.ext.commands import Bot
from discord import Interaction, app_commands
from core.cog_base import CogBase
from api.clients import openai_client

class Greetings(CogBase, name="Greetings module", description="Bot presentations for testing purposes"):
    def __init__(self, bot: Bot):
        super().__init__(bot)

    @app_commands.command(name="ping", description="For test purposes")
    async def ping(self, interaction: Interaction) -> None:
        await interaction.response.send_message(f"Pong!🏓 {round(self.bot.latency * 1000)}ms")


    @app_commands.command(name="hello", description="Sends greeting")
    async def hello(self, interaction: Interaction) -> None:
        completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say \"Hello!\" in a random language",
                }
            ],
            max_tokens = 10,
            model="gpt-3.5-turbo",
        )
        await interaction.response.send_message(completion.choices[0].message.content)

async def setup(bot: Bot) -> None:
    await Greetings(bot).setup()
