import json
from datetime import datetime
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "recommendations.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)

def log_recommendation(request, recommendations):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": request.session_id,  # 🔴 ADD THIS
        "city": request.city,
        "situation": request.answers.situation,
        "craving": request.answers.craving,
        "constraints": request.answers.constraints,
        "recommendations": [
            {
                "dish_id": r["dish_id"],
                "score": r["score"],
                "rank": idx + 1
            }
            for idx, r in enumerate(recommendations)
        ]
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
