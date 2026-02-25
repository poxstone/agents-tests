import vertexai
from vertexai import agent_engines
import argparse

# 1. Configuración inicial
PROJECT_ID = "bluetab-colombia-data-qa"
PROJECT_NUMBER = "886084989545"
LOCATION = "us-central1"
AGENT_ID = "2537438640930291712"
RESOURCE_NAME = f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/reasoningEngines/{AGENT_ID}"

vertexai.init(project=PROJECT_ID, location=LOCATION)

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