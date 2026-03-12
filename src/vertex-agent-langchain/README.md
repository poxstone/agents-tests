# Model Agent Engine Test
## Install

```bash
python3 -m virtualenv .venv;
source .venv;
pip install -r requirements.txt;
```

## Deploy

- Update constantnts into main.py
```bash
python agent_test/agent.py;

.venv/lib/python3.12/site-packages/google/cloud/aiplatform/models.py:52: FutureWarning: Support for google-cloud-storage < 3.0.0 will be removed in a future version of google-cloud-aiplatform. Please upgrade to google-cloud-storage >= 3.0.0.
  from google.cloud.aiplatform.utils import gcs_utils
Using bucket PROJECT_GCP-staging-bucket
Writing to gs://PROJECT_GCP-staging-bucket/reasoning_engine/reasoning_engine.pkl
Writing to gs://PROJECT_GCP-staging-bucket/reasoning_engine/requirements.txt
Creating in-memory tarfile of extra_packages
Writing to gs://PROJECT_GCP-staging-bucket/reasoning_engine/dependencies.tar.gz
Creating ReasoningEngine
Create ReasoningEngine backing LRO: projects/PROJECT_NUMBER/locations/us-central1/reasoningEngines/5914153199039676416/operations/3287300906739040256
ReasoningEngine created. Resource name: projects/PROJECT_NUMBER/locations/us-central1/reasoningEngines/5914153199039676416
To use this ReasoningEngine in another session:
reasoning_engine = vertexai.preview.reasoning_engines.ReasoningEngine('projects/PROJECT_NUMBER/locations/us-central1/reasoningEngines/5914153199039676416')
Despliegue finalizado: projects/PROJECT_NUMBER/locations/us-central1/reasoningEngines/5914153199039676416
```


## Consume

- Update constantnts into main.py
```bash
python client/client.py222;
python client/client.py --session="usuario_1" "hola como estas? me recuerdas?";
```
