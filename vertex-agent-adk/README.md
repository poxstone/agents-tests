
# ADK to Agent Engine Test

## Prepare environment

```bash
# install globally
export PATH=$PATH:"/home/${USER}/.local/bin";
python3 -m pip install -r ./requirements.txt;
```

## Env file

```bash
cat << EOF > .env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=bluetab-colombia-data-qa
GOOGLE_CLOUD_LOCATION=us-central1
MODEL=gemini-2.5-flash
EOF

cp .env agente_cortes/.env;
```

## Run Local

```bash
adk web;
```

## Test preguntas

- Mi nombre es pedro y tengo 52 años soy de colombia
- Hola como estas? me recuerdas?

## Deploy

```bash
adk deploy agent_engine agente_cortes;
```

## Consume

- Update constantnts into main.py

```bash
python ./client/client.py --session="usuario_1" "mi nombre es pedro y tengo 52 años soy de colombia";
python ./client/client.py --session="usuario_1" "hola como estas? me recuerdas?";
```