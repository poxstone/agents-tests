
# ADK to Agent Engine Test

## Prepare environment

### Install uv (if not installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup project

```bash
# Install dependencies with uv
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

## Env file

```bash
# Extract project information from gcloud
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export GOOGLE_CLOUD_PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")

# Create .env file
cat << EOF > .env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT
PROJECT_NUMBER=$GOOGLE_CLOUD_PROJECT_NUMBER
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=TRUE
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=TRUE
MODEL=gemini-2.5-flash

# Client configuration
AGENT_ID=5741675009013710848
EOF

# Copy .env to required directories
cp .env agente_cortes/.env
cp .env client/.env
```

## Run Local

```bash
# Make sure the virtual environment is activated
gcloud auth application-default login
uv run adk web

#opcional
docker run -it -d --rm --name redis-service -p 6379:6379 --platform linux/amd64 redis:7.2-alpine redis-server
redis-cli -h 127.0.0.1 -p 6379

docker run -it -d --rm --name redis-service -p 6379:6379 -e POSTGRES_PASSWORD=MyPassXample -e POSTGRES_DB=vectordb --platform pgvector/pgvector:pg16 redis-server


# --requirepass MyPassXample
```

## Test preguntas

- Mi nombre es pedro y tengo 52 años soy de colombia
- Hola como estas? me recuerdas?

## Deploy

Para configurar opciones avanzadas durante el despliegue a Vertex AI Agent Engine, debes editar el archivo `.agent_engine_config.json` dentro del directorio del agente (por ejemplo, `agente_cortes/.agent_engine_config.json`). Este archivo soporta múltiples configuraciones como límites de recursos, variables de entorno, seguridad y conexión a VPC usando PSC.

A continuación, un ejemplo completo con todas las opciones principales (nota: JSON no soporta comentarios nativamente, asegúrate de removerlos si copias el archivo literal, este es un prototipo ilustrativo):

```json
{
  // ----------------------------------------------------------------------
  // Identidad y Permisos
  // ----------------------------------------------------------------------
  
  // Cuenta de servicio que usará el agente. Ignorado si se usa agent_identity.
  "service_account": "tu-cuenta-de-servicio@tu-proyecto.iam.gserviceaccount.com",
  
  // Tipo de identidad: "IDENTITY_TYPE_UNSPECIFIED", "SERVICE_ACCOUNT" o "AGENT_IDENTITY"
  "identity_type": "SERVICE_ACCOUNT",

  // ----------------------------------------------------------------------
  // Recursos y Escalabilidad
  // ----------------------------------------------------------------------
  
  // Límites de recursos por contenedor. CPU soportada: "1", "2", "4", "6", "8". 
  // Memoria soportada: "1Gi", "2Gi"... "32Gi"... Defaults: cpu=4, memory=4Gi
  "resource_limits": {
    "cpu": "4",
    "memory": "4Gi"
  },
  
  // Mínimo de instancias siempre corriendo (0 a 10). Default 1.
  "min_instances": 1,
  
  // Máximo de instancias (1 a 1000, o hasta 100 si usa PSC/VPC-SC). Default 100.
  "max_instances": 100,
  
  // Concurrencia por contenedor (recomendado: 2 * cpu + 1). Default 9.
  "container_concurrency": 9,

  // ----------------------------------------------------------------------
  // Variables de Entorno y Seguridad
  // ----------------------------------------------------------------------
  
  // Variables de entorno estándar
  "env": [
    { "name": "MI_VARIABLE", "value": "mi_valor" }
  ],
  
  // Variables de entorno desde Cloud Secret Manager
  "secret_env": [
    { "name": "API_KEY", "secret": "projects/12345/secrets/mi-secreto/versions/latest" }
  ],
  
  // Especificación para llaves de encriptación manejadas por el cliente (CMEK)
  "encryption_spec": {
    "kms_key_name": "projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY_NAME"
  },

  // ----------------------------------------------------------------------
  // Redes (Private Service Connect - PSC-I)
  // ----------------------------------------------------------------------
  
  "psc_interface_config": {
    // Adjunto de red (Network Attachment) para la VPC
    "network_attachment": "projects/tu-proyecto/regions/us-central1/networkAttachments/agent-engine-net-attach",
    
    // Configuración opcional para resolución DNS privada a través de VPC
    "dns_peering_configs": [
      {
        "domain": "mi-dominio-interno.corp.",
        "target_project": "proyecto-red-destino",
        "target_network": "red-vpc-destino"
      }
    ]
  },

  // ----------------------------------------------------------------------
  // Otras configuraciones
  // ----------------------------------------------------------------------
  
  // Paquetes o requerimientos adicionales de Python a instalar durante build
  "requirements": [
    "requests",
    "google-cloud-aiplatform"
  ],
  
  // "STABLE" (por defecto) o "EXPERIMENTAL" para habilitar modo preview del server
  "agent_server_mode": "STABLE"
}
```

### Configurar Acceso a VPC (Private Service Connect)

Para permitir que el agente se conecte a una red VPC privada (por ejemplo, para consultar bases de datos internas), Vertex AI Agent Engine utiliza Private Service Connect (PSC). Debes realizar la siguiente configuración en GCP:

1. **Crear una subred (si no existe)**:
   ```bash
   gcloud compute networks subnets create psc-agent-engine-subnet \
       --network=default \
       --region=us-central1 \
       --range=10.10.0.0/28 \
       --project=tu-proyecto
   ```

2. **Crear un Adjunto de Red (Network Attachment)** asociado a la subred creada:
   ```bash
   gcloud compute network-attachments create agent-engine-net-attach \
       --region=us-central1 \
       --subnets=psc-agent-engine-subnet \
       --connection-preference=ACCEPT_AUTOMATIC \
       --project=tu-proyecto
   ```

3. **Asignar Permisos**: Es **indispensable** asegurar que la cuenta de servicio predeterminada de AI Platform (`service-[PROJECT_NUM]@gcp-sa-aiplatform.iam.gserviceaccount.com`) tenga el permiso `compute.networkAttachments.update` sobre el Network Attachment para que pueda conectarse adecuadamente.

4. **Actualizar la configuración del Agente**: Añadir la configuración del Network Attachment en `.agent_engine_config.json` bajo la propiedad `psc_interface_config`:
   ```json
   {
     "service_account": "tu-cuenta-de-servicio@tu-proyecto.iam.gserviceaccount.com",
     "psc_interface_config": {
       "network_attachment": "projects/tu-proyecto/regions/us-central1/networkAttachments/agent-engine-net-attach"
     }
   }
   ```

Luego puedes hacer el despliegue:

```bash
uv run adk deploy agent_engine "agente_cortes"
```

## Consume

- Update constants into main.py

```bash
uv run python ./client/client.py --session="usuario_1" "mi nombre es pedro y tengo 52 años soy de colombia"
uv run python ./client/client.py --session="usuario_1" "hola como estas? me recuerdas?"
uv run python ./client/client.py --session="usuario_1" "que hora es?"
uv run python ./client/client.py --session="usuario_1" "lista los buckets de mi proyecto"
```

## permisos requeridos

- PROJECT_AGENT
-- sa-agent@PROJECT_AGENT.gserviceaccount.com
--- Vertex AI User
--- Service Usage Consumer

- PROJECT_NETWORK
-- service-PROJECT_AGENT_NUMBER@gcp-sa-aiplatform.iam.gserviceaccount.com
--- Vertex AI Service Admin
--- Compute Network Admin

