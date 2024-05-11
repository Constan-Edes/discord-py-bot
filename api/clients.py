from openai import OpenAI
from core.config import settings

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
