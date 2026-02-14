import json
from datetime import datetime
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "feedback.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)

def log_feedback(restaurant_id, session_id, dish_id, action):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "restaurant_id": restaurant_id,
        "session_id": session_id,
        "dish_id": dish_id,
        "action": action  # "click" or "order"
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
