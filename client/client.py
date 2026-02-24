import sys
import argparse
import vertexai
from vertexai.preview import reasoning_engines

# 1. Configuración (Usa los datos de tu despliegue)
PROJECT_ID = "bluetab-colombia-data-qa"
PROJECT_NUMBER = "886084989545"
LOCATION = "us-central1"
RESOURCE_ID = "8925372499890274304"
RESOURCE_NAME = f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/reasoningEngines/{RESOURCE_ID}"



def main():

    try:
        # 1. Configurar el parseador de argumentos
        parser = argparse.ArgumentParser(description="Consulta a mi Agente de Vertex AI")
        parser.add_argument(
            "prompt", 
            type=str, 
            help="El texto o pregunta que le quieres enviar al agente"
        )
        parser.add_argument("--session", type=str, default="usuario_123")
        
        # 2. Inicializar el SDK
        vertexai.init(project=PROJECT_ID, location=LOCATION)

        # 3. Cargar el agente desplegado
        # Esto no vuelve a desplegar nada, solo crea una referencia al microservicio activo
        remote_agent = reasoning_engines.ReasoningEngine(RESOURCE_NAME)

        # 4. Consultar el agente
        # Importante: El nombre del argumento (input) debe ser el mismo que definiste 
        # en el método query() de tu clase.
        args = parser.parse_args()
    
        response = remote_agent.query(
            input=args.prompt,
            session_id=args.session
            )
        print(f"\n[Sesión: {args.session}]\nRespuesta: {response}")
    except Exception as e:
        print(f"Error al consultar el agente: {e}")
    

if __name__ == "__main__":
    main()