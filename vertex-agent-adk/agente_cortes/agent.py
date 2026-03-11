import os
import urllib.request
import urllib.error
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import storage
import redis

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

def fetch_website_headers(protocol: str = "https", domain: str = "www.eltiempo.com", port: int = 443) -> str:
    """
    Realiza una petición a un sitio web y devuelve sus encabezados HTTP (Headers).
    
    Args:
        protocol (str): Protocolo a usar (http o https). Por defecto https.
        domain (str): El dominio del sitio web. Por defecto www.eltiempo.com.
        port (int): El puerto a consultar. Por defecto 443.
        
    Returns:
        str: Los encabezados de la respuesta HTTP en formato texto y una parte del body, o un mensaje de error si falla.
    """
    # Construcción de la URL
    if (protocol == "https" and port == 443) or (protocol == "http" and port == 80):
        url = f"{protocol}://{domain}"
    else:
        url = f"{protocol}://{domain}:{port}"
        
    try:
        # Se envía un User-Agent de navegador para evitar bloqueos básicos
        req = urllib.request.Request(url, method="GET", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            headers = str(response.headers)
            try:
                # Leemos un máximo de 2000 caracteres para evitar saturar el contexto del agente
                body = response.read(2000).decode('utf-8')
            except Exception:
                body = "<No se pudo decodificar el body a texto>"
            return f"--- HEADERS ---\n{headers}\n--- BODY (Truncado) ---\n{body}"
    except urllib.error.URLError as e:
        return f"Error al acceder a {url}: {e.reason}"
    except Exception as e:
        return f"Error inesperado al acceder a {url}: {str(e)}"

def save_to_redis(key: str, value: str) -> str:
    """
    Guarda un valor en Redis usando el host y password de variables de entorno (por defecto host 127.0.0.1).
    
    Args:
        key (str): La clave bajo la cual guardar el valor.
        value (str): El valor a guardar.
        
    Returns:
        str: Un mensaje de confirmación de éxito o el error.
    """
    try:
        # Recuperar password y host de la variable de entorno
        redis_host = os.getenv("REDIS_HOST", "10.0.0.229")
        
        # Se conecta a redis
        client = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
        client.set(key, value)
        return f"Éxito: Se ha guardado el valor en la clave '{key}'."
    except Exception as e:
        return f"Error al guardar en Redis: {str(e)}"

root_agent = Agent(
    name="agente_cortes",
    description="Asistente recuerda",
    model=Gemini(
        model=os.getenv("MODEL", "gemini-2.5-flash"),
        retry_options=retry_options
    ),
    instruction="Eres un asistente con memoria persistente, si te dan datos personales siempre respondes dirigiendote formalmente con su nombre y algo que te haya contado. siempre estas atento",
    tools=[get_current_time, list_gcs_buckets, fetch_website_headers, save_to_redis],
)