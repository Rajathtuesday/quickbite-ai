import random
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

SESSIONS = 500

cities = ["bangalore"]

situations = [
    "office_lunch",
    "treat_myself",
    "lazy_tired",
    "light_healthy",
    "evening_snack",
    "celebration"
]

cravings = [
    "spicy",
    "creamy",
    "sweet",
    "healthy",
    "fried"
]

constraints_pool = [
    [],
    ["veg_only"],
    ["under_250"],
    ["veg_only", "under_250"]
]

def simulate_user_behavior(dish_id, situation, craving):
    """
    Simulate realistic click probability
    """

    # Bias rules to create learnable patterns

    if situation == "office_lunch" and craving == "spicy" and dish_id in ["d1", "d8", "d9"]:
        return 0.6

    if situation == "lazy_tired" and craving == "sweet" and dish_id in ["d10", "d11"]:
        return 0.7

    if situation == "treat_myself" and craving == "creamy" and dish_id in ["d4"]:
        return 0.65

    # default weak click probability
    return 0.05


for i in range(SESSIONS):

    session_id = f"sim_{i}"

    payload = {
        "city": random.choice(cities),
        "session_id": session_id,
        "answers": {
            "situation": random.choice(situations),
            "craving": random.choice(cravings),
            "constraints": random.choice(constraints_pool)
        }
    }

    try:
        response = requests.post(f"{BASE_URL}/v1/recommend", json=payload)
        data = response.json()

        for item in data["top_picks"]:

            dish_id = item["dish_id"]

            click_prob = simulate_user_behavior(
                dish_id,
                payload["answers"]["situation"],
                payload["answers"]["craving"]
            )

            if random.random() < click_prob:

                # log click
                requests.post(
                    f"{BASE_URL}/v1/feedback",
                    json={
                        "session_id": session_id,
                        "dish_id": dish_id,
                        "action": "click"
                    }
                )

                # 50% chance order after click
                if random.random() < 0.5:
                    requests.post(
                        f"{BASE_URL}/v1/feedback",
                        json={
                            "session_id": session_id,
                            "dish_id": dish_id,
                            "action": "order"
                        }
                    )

    except Exception as e:
        print("Error:", e)

    if i % 50 == 0:
        print(f"Simulated {i} sessions")

print("✅ Simulation complete")
