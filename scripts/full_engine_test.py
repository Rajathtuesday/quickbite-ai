import requests
import json
import time
import random
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

REPORT = {
    "timestamp": datetime.utcnow().isoformat(),
    "functional_tests": {},
    "constraint_tests": {},
    "margin_sensitivity_tests": {},
    "stress_test": {}
}

# ======================================================
# Helper
# ======================================================

def post(endpoint, payload=None, params=None):
    try:
        r = requests.post(f"{BASE_URL}{endpoint}", json=payload, params=params)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"error": str(e)}

# ======================================================
# 1️⃣ Functional Mode Test
# ======================================================

print("Running functional test...")

menu_payload = {
    "restaurant_id": "rest_test_engine",
    "menu": [
        {
            "dish_id": "a_high_margin_creamy",
            "name": "Creamy Paneer",
            "price": 300,
            "margin": 120,
            "tags": ["veg", "creamy", "north_indian"],
            "popularity": 0.5
        },
        {
            "dish_id": "b_spicy_low_margin",
            "name": "Spicy Dosa",
            "price": 120,
            "margin": 30,
            "tags": ["veg", "spicy", "south_indian"],
            "popularity": 0.6
        }
    ]
}

post("/v1/upload_menu", menu_payload)

recommend_payload = {
    "restaurant_id": "rest_test_engine",
    "city": "bangalore",
    "session_id": "functional_test",
    "answers": {
        "situation": "office_lunch",
        "craving": "spicy",
        "constraints": []
    }
}

status_click, click_data = post("/v1/recommend", recommend_payload, {"mode": "click"})
status_profit, profit_data = post("/v1/recommend", recommend_payload, {"mode": "profit"})

REPORT["functional_tests"] = {
    "click_top": click_data.get("top_picks", []),
    "profit_top": profit_data.get("top_picks", [])
}

# ======================================================
# 2️⃣ Constraint Test
# ======================================================

print("Running constraint test...")

recommend_payload["answers"]["constraints"] = ["under_250"]

status_constraint, constraint_data = post("/v1/recommend", recommend_payload)

REPORT["constraint_tests"] = {
    "response": constraint_data.get("top_picks", [])
}

# ======================================================
# 3️⃣ Margin Sensitivity Test
# ======================================================

print("Running margin sensitivity test...")

menu_payload["menu"][0]["margin"] = 10
menu_payload["menu"][1]["margin"] = 150

post("/v1/upload_menu", menu_payload)

recommend_payload["answers"]["constraints"] = []

status_margin, margin_data = post("/v1/recommend", recommend_payload, {"mode": "profit"})

REPORT["margin_sensitivity_tests"] = {
    "top_picks": margin_data.get("top_picks", [])
}

# ======================================================
# 4️⃣ Stress Test
# ======================================================

print("Running stress test...")

start_time = time.time()
errors = 0
success = 0

for i in range(300):
    recommend_payload["session_id"] = f"stress_{i}"

    status, data = post("/v1/recommend", recommend_payload)

    if status != 200:
        errors += 1
    else:
        success += 1

end_time = time.time()

REPORT["stress_test"] = {
    "requests": 300,
    "success": success,
    "errors": errors,
    "duration_sec": round(end_time - start_time, 2)
}

# ======================================================
# Save Report
# ======================================================

with open("logs/full_engine_report.json", "w", encoding="utf-8") as f:
    json.dump(REPORT, f, indent=4)

print("\n✅ Full engine test completed.")
print("Report saved to logs/full_engine_report.json")
