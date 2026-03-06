import vertexai
from vertexai import agent_engines
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
# Buscar .env en vertex-agent-adk/client/.env
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✓ Loaded .env from: {env_path}")
else:
    print(f"⚠ Warning: .env file not found at {env_path}")
    load_dotenv()  # Intenta cargar desde el directorio actual o variables del sistema

# 1. Configuración inicial
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
PROJECT_NUMBER = os.getenv("PROJECT_NUMBER")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
AGENT_ID = os.getenv("AGENT_ID")
RESOURCE_NAME = f"projects/{PROJECT_NUMBER}/locations/{GOOGLE_CLOUD_LOCATION}/reasoningEngines/{AGENT_ID}"

# Debug: Mostrar variables cargadas
print(f"PROJECT: {GOOGLE_CLOUD_PROJECT}")
print(f"PROJECT_NUMBER: {PROJECT_NUMBER}")
print(f"LOCATION: {GOOGLE_CLOUD_LOCATION}")
print(f"AGENT_ID: {AGENT_ID}")
print()

vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)

def query_adk_agent(prompt, session_id):
        
    try:
        # Cargamos el agente
        remote_agent = agent_engines.AgentEngine(AGENT_ID)
        session = remote_agent.create_session(user_id=session_id)
        
        print(f"Iniciando consulta al agente {AGENT_ID}...")

        response_parts = []
        events = remote_agent.stream_query(
            message=prompt, 
            user_id=session_id,
            session_id=session["id"]
        )

        for event in events:
            for part in event["content"]["parts"]:
                if "text" in part:
                    response_parts.append(part["text"])
        response = "".join(response_parts)

        return response

    except Exception as e:
        return f"Error crítico: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query a Vertex AI Agent Engine.")
    parser.add_argument("prompt", type=str, help="The prompt for the agent.")
    parser.add_argument("--session", type=str, default="sesion_usuario_001", 
                        help="The session ID for the agent. Defaults to 'sesion_usuario_001'.")
    
    args = parser.parse_args()

    resultado = query_adk_agent(args.prompt, args.session)
    
    print("\nRespuesta del Agente:")
    print("-" * 20)
    print(resultado)