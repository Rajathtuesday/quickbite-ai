import json
from collections import defaultdict
from app.data import DISHES

RECO_FILE = "logs/recommendations.jsonl"
FEEDBACK_FILE = "logs/feedback.jsonl"

dish_lookup = {d["dish_id"]: d for d in DISHES}

# ----------------------------
# Sessions Served
# ----------------------------
session_ids = set()

with open(RECO_FILE, "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        session_ids.add(entry["session_id"])

total_sessions = len(session_ids)

# ----------------------------
# Orders & Revenue
# ----------------------------
total_orders = 0
total_revenue = 0

with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)

        if entry["action"] == "order":
            total_orders += 1
            dish_id = entry["dish_id"]

            if dish_id in dish_lookup:
                total_revenue += dish_lookup[dish_id]["margin"]

# ----------------------------
# Metrics
# ----------------------------
conversion_rate = (
    (total_orders / total_sessions) * 100
    if total_sessions > 0 else 0
)

avg_revenue_per_session = (
    total_revenue / total_sessions
    if total_sessions > 0 else 0
)

avg_revenue_per_order = (
    total_revenue / total_orders
    if total_orders > 0 else 0
)

# ----------------------------
# Output
# ----------------------------

print("\n=== REVENUE ANALYTICS ===")
print(f"Total Sessions Served: {total_sessions}")
print(f"Total Orders: {total_orders}")
print(f"Conversion Rate: {conversion_rate:.2f}%")
print(f"Total Revenue: ₹{total_revenue}")
print(f"Avg Revenue per Session: ₹{avg_revenue_per_session:.2f}")
print(f"Avg Revenue per Order: ₹{avg_revenue_per_order:.2f}")
