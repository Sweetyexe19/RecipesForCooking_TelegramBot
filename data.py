import json
import os

FAVORITES_FILE = "favorites.json"
VIEWED_FILE = "viewed.json"

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

favorites = load_data(FAVORITES_FILE)
viewed = load_data(VIEWED_FILE)