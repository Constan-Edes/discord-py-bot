from discord import Interaction
from core.config import settings

def is_owner(interaction: Interaction) -> bool:
    return interaction.user.id is settings.OWNER_ID 

