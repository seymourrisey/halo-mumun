import os
import json

CONFIG_PATH = "data/mumun_config.json"

def save_api_key(key: str):
    os.makedirs("data", exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"groq_api_key": key}, f)

def load_api_key() -> str | None:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            data = json.load(f)
            return data.get("groq_api_key")
    return None

def delete_api_key():
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)

should_cancel = False