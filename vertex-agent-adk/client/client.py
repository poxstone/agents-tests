import vertexai
from vertexai import agent_engines

# 1. Configuración inicial
PROJECT_ID = "bluetab-colombia-data-qa"
PROJECT_NUMBER = "886084989545"
LOCATION = "us-central1"
AGENT_ID = "2537438640930291712"
RESOURCE_NAME = f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/reasoningEngines/{AGENT_ID}"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def query_adk_agent(prompt):
        
    try:
        # Cargamos el agente
        remote_agent = agent_engines.AgentEngine(AGENT_ID)
        session = remote_agent.create_session(user_id="sesion_usuario_001")
        
        print(f"Iniciando consulta al agente {AGENT_ID}...")

        response_parts = []
        events = remote_agent.stream_query(
            message=prompt, 
            user_id="sesion_usuario_001",
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
    prompt_usuario = "¿Puedes darme un resumen de los últimos logs?"
    resultado = query_adk_agent(prompt_usuario)
    
    print("\nRespuesta del Agente:")
    print("-" * 20)
    print(resultado)