import os
import json
import re

CONFIG_PATH = "data/mumun_config.json"

def load_api_key() -> str:
    if not os.path.exists(CONFIG_PATH):
        os.makedirs("data", exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump({"groq_api_key": ""}, f)

    with open(CONFIG_PATH) as f:
        data = json.load(f)
        return data.get("groq_api_key", "")

def is_valid_api_key(key: str) -> bool:
    return bool(re.fullmatch(r"gsk_[a-zA-Z0-9]{20,}", key))

def save_api_key(key: str):
    os.makedirs("data", exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"groq_api_key": key}, f)

def delete_api_key():
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)

# Untuk kontrol cancel dari luar
should_cancel = False
