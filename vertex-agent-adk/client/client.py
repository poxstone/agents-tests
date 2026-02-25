import vertexai
from vertexai.preview import reasoning_engines

# 1. Configuración inicial
PROJECT_ID = "bluetab-colombia-data-qa"
PROJECT_NUMBER = "886084989545"
LOCATION = "us-central1"
AGENT_ID = "2537438640930291712"
RESOURCE_NAME = f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/reasoningEngines/{AGENT_ID}"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def query_adk_agent(prompt):
    # Definimos el nombre completo del recurso
    resource_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ID}"
    
    try:
        # Cargamos el agente
        remote_agent = reasoning_engines.ReasoningEngine(resource_name)
        
        print(f"Iniciando consulta al agente {AGENT_ID}...")

        # SOLUCIÓN: Usamos el método interno de consulta que no depende del registro dinámico
        # Basado en tus 'schemas', los parámetros requeridos son 'message' y 'user_id'
        
        # Intentamos con la llamada directa de 'query' del cliente subyacente
        response = remote_agent.query(
            message=prompt, 
            user_id="sesion_usuario_001"
        )

        return response

    except Exception as e:
        # Si .query() falla, forzamos la llamada al método de stream de forma manual
        try:
            print("Probando método de fallback...")
            # Esta es la forma más "cruda" de llamar al agente
            return remote_agent._resource.stream_query(
                message=prompt, 
                user_id="sesion_usuario_001"
            )
        except:
            return f"Error crítico: {str(e)}"

if __name__ == "__main__":
    prompt_usuario = "¿Puedes darme un resumen de los últimos logs?"
    resultado = query_adk_agent(prompt_usuario)
    
    print("\nRespuesta del Agente:")
    print("-" * 20)
    print(resultado)