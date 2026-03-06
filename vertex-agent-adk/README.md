
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
cat << EOF > .env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=TRUE
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=TRUE
MODEL=gemini-2.5-flash
EOF

cp .env agente_cortes/.env
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

```bash
uv run adk deploy agent_engine agente_cortes
```

## Consume

- Update constants into main.py

```bash
uv run python ./client/client.py --session="usuario_1" "mi nombre es pedro y tengo 52 años soy de colombia"
uv run python ./client/client.py --session="usuario_1" "hola como estas? me recuerdas?"
```