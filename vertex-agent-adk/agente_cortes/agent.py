import os
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import storage

from google.adk import Agent
from google.adk.models import Gemini
from google.genai import types

retry_options = types.HttpRetryOptions(initial_delay=1, attempts=6)

load_dotenv()

def get_current_time() -> str:
    """
    Devuelve la hora actual del sistema.

    Returns:
        str: La hora actual.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def list_gcs_buckets(project_id: str = None) -> list[str]:
    """
    Lista los buckets de Google Cloud Storage en el proyecto especificado.
    
    Args:
        project_id (str, optional): El ID del proyecto. Si no se indica, usa el proyecto por defecto configurado en el entorno.

    Returns:
        list[str]: Una lista con los nombres de los buckets. Si hay un error, devuelve un mensaje de error.
    """
    try:
        client = storage.Client(project=project_id) if project_id else storage.Client()
        buckets = client.list_buckets()
        return [bucket.name for bucket in buckets]
    except Exception as e:
        return [f"Error al listar buckets: {str(e)}"]

root_agent = Agent(
    name="agente_cortes",
    description="Asistente recuerda",
    model=Gemini(
        model=os.getenv("MODEL", "gemini-2.5-flash"),
        retry_options=retry_options
    ),
    instruction="Eres un asistente con memoria persistente, si te dan datos personales siempre respondes dirigiendote formalmente con su nombre y algo que te haya contado. siempre estas atento",
    tools=[get_current_time, list_gcs_buckets],
)