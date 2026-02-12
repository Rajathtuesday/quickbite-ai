import json
from collections import defaultdict

from app.data import DISHES


RECO_FILE = "logs/recommendations.jsonl"
FEEDBACK_FILE = "logs/feedback.jsonl"
OUTPUT_FILE = "logs/training_data.jsonl"

# Create dish lookup
dish_lookup = {d["dish_id"]: d for d in DISHES}

feedback_map = defaultdict(lambda: {"click": False, "order": False})

# -------------------------------
# Load feedback
# -------------------------------

with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        key = (entry["session_id"], entry["dish_id"])
        feedback_map[key][entry["action"]] = True

# -------------------------------
# Build training data
# -------------------------------

with open(RECO_FILE, "r", encoding="utf-8") as rf, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as out:

    for line in rf:
        rec = json.loads(line)

        session_id = rec["session_id"]

        for r in rec["recommendations"]:
            dish_id = r["dish_id"]
            dish = dish_lookup[dish_id]

            feedback = feedback_map[(session_id, dish_id)]

            tags = dish["tags"]

            row = {
                "city": rec["city"],
                "context_combo": rec["situation"] + "_" + rec["craving"],

                # Dish features
                "is_spicy": int("spicy" in tags),
                "is_creamy": int("creamy" in tags),
                "is_sweet": int("sweet" in tags),
                "is_fried": int("fried" in tags),
                "is_healthy": int("healthy" in tags),
                "is_indulgent": int("indulgent" in tags),
                "is_south_indian": int("south_indian" in tags),
                "is_north_indian": int("north_indian" in tags),
                "is_street_food": int("street_food" in tags),

                "popularity": dish["popularity"],
                "price_bucket": int(dish["price"] // 100),

                "clicked": int(feedback["click"])
            }

            out.write(json.dumps(row) + "\n")

print("✅ Training data written")
