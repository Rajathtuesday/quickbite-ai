import random
from app.data import DISHES
from app.ml_scoring import ml_score_dish

SESSIONS = 500

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

def simulate_click(dish, situation, craving):
    # Same behavior logic as simulate_session
    if situation == "office_lunch" and craving == "spicy" and dish["dish_id"] in ["d1","d8","d9"]:
        return random.random() < 0.6
    if situation == "lazy_tired" and craving == "sweet" and dish["dish_id"] in ["d10","d11"]:
        return random.random() < 0.7
    if situation == "treat_myself" and craving == "creamy" and dish["dish_id"] in ["d4"]:
        return random.random() < 0.65

    return random.random() < 0.05


def run_strategy(strategy_name):

    total_revenue = 0
    total_orders = 0

    for _ in range(SESSIONS):

        situation = random.choice(situations)
        craving = random.choice(cravings)

        if strategy_name == "random":
            ranked = random.sample(DISHES, len(DISHES))

        elif strategy_name == "popularity":
            ranked = sorted(DISHES, key=lambda d: d["popularity"], reverse=True)

        elif strategy_name == "ml_profit":
            ranked = sorted(
                DISHES,
                key=lambda d: ml_score_dish(
                    city="bangalore",
                    situation=situation,
                    craving=craving,
                    dish_id=d["dish_id"]
                ) * d["margin"],
                reverse=True
            )

        else:
            raise ValueError("Unknown strategy")

        top3 = ranked[:3]

        for dish in top3:
            if simulate_click(dish, situation, craving):
                total_orders += 1
                total_revenue += dish["margin"]

    return total_revenue, total_orders


strategies = ["random", "popularity", "ml_profit"]

results = {}

for s in strategies:
    revenue, orders = run_strategy(s)
    results[s] = {
        "revenue": revenue,
        "orders": orders,
        "avg_revenue_per_session": round(revenue / SESSIONS, 2)
    }

print("\n=== REVENUE COMPARISON ===\n")

for k, v in results.items():
    print(f"{k.upper()}")
    print(f"Revenue: ₹{v['revenue']}")
    print(f"Orders: {v['orders']}")
    print(f"Avg per session: ₹{v['avg_revenue_per_session']}")
    print()

ml = results["ml_profit"]["revenue"]
pop = results["popularity"]["revenue"]

uplift = ((ml - pop) / pop) * 100 if pop != 0 else 0

print(f"ML vs Popularity Revenue Lift: {round(uplift,2)}%")
