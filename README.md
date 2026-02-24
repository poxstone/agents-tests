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
```

## Consume

- Update constantnts into main.py
```bash
python client/client.py "mi nombre es pedro y tengo 52 años soy de colombia" --session="cliente123";
python client/client.py "quiero viajar a un lugar cercano que a mi edad sea prudente" --session="cliente123";
```
