import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.models import Gemini
from google.genai import types

retry_options = types.HttpRetryOptions(initial_delay=1, attempts=6)

load_dotenv()

root_agent = Agent(
    name="agente_cordial",
    description="Asistente recuerda",
    model=Gemini(
        model=os.getenv("MODEL", "gemini-2.5-flash"),
        retry_options=retry_options
    ),
    instruction="Eres un asistente con memoria persistente, si te dan datos personales siempre respondes dirigiendote formalmente con su nombre y algo que te haya contado. siempre estas atento",
)