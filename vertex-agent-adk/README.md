
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
uv run adk web
```

## Test preguntas

- Mi nombre es pedro y tengo 52 años soy de colombia
- Hola como estas? me recuerdas?

## Deploy

Para configurar una cuenta de servicio específica durante el despliegue a Vertex AI Agent Engine, debes editar el archivo `.agent_engine_config.json` dentro del directorio del agente (por ejemplo, `agente_cortes/.agent_engine_config.json`) y agregar el campo `service_account`:

```json
{
  "service_account": "tu-cuenta-de-servicio@tu-proyecto.iam.gserviceaccount.com"
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