import sys
import argparse
import vertexai
from vertexai.preview import reasoning_engines

# 1. Configuración (Usa los datos de tu despliegue)
PROJECT_ID = "bluetab-colombia-data-qa"
LOCATION = "us-central1"
AGENT_DISPLAY_NAME = "agente-test-01" # El nombre que usaste al desplegar

def main():

    try:
        # 1. Configurar el parseador de argumentos
        parser = argparse.ArgumentParser(description="Consulta a mi Agente de Vertex AI")
        # Usamos nargs='+' para capturar todo el texto del prompt como una lista de palabras
        parser.add_argument( "prompt", nargs='+', type=str,  help="El texto o pregunta que le quieres enviar al agente")
        parser.add_argument("--session", type=str, default="usuario_123")
        args = parser.parse_args()

        # Unimos la lista de palabras para reconstruir el prompt completo
        prompt_text = " ".join(args.prompt)
        
        # 2. Inicializar el SDK
        vertexai.init(project=PROJECT_ID, location=LOCATION)

        # 3. Cargar el agente desplegado por su nombre para asegurar que es el correcto
        existing_agents = reasoning_engines.ReasoningEngine.list(
            filter=f'display_name="{AGENT_DISPLAY_NAME}"'
        )
        if not existing_agents:
            print(f"Error: No se encontró ningún agente con el nombre '{AGENT_DISPLAY_NAME}'.")
            print("Asegúrate de haber desplegado el agente desde 'vertex-agent-langchain/agent_test/agent.py'.")
            sys.exit(1)
        
        remote_agent = existing_agents[0]
        
        # 4. Consultar el agente usando el método query() del ReasoningEngine.
        # El input debe ser un diccionario que mapea a los argumentos del método query del agente.
        response = remote_agent.query(
            input={"input": prompt_text, "session_id": args.session}
        )

        # La respuesta es directamente el contenido que retorna el agente.
        full_response = response

        print(f"\n[Sesión: {args.session}]\nRespuesta: {full_response}")
    except Exception as e:
        print(f"Error al consultar el agente: {e}")
    

if __name__ == "__main__":
    main()