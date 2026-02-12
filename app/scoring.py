from datetime import datetime, date
from app.data import FESTIVALS

# -------------------------------
# Context helpers
# -------------------------------

def get_time_bucket():
    hour = datetime.now().hour
    if 6 <= hour < 11:
        return "morning"
    elif 11 <= hour < 16:
        return "lunch"
    elif 16 <= hour < 19:
        return "evening"
    else:
        return "night"


def get_day_type():
    return "weekday" if datetime.now().weekday() < 5 else "weekend"


def get_festival():
    today = date.today().isoformat()
    return FESTIVALS.get(today)


# -------------------------------
# Scoring logic
# -------------------------------

def score_dish(dish, answers, city_bias):
    score = 0.0
    reasons = []

    # 1️⃣ Craving — STRONG signal
    if answers["craving"] in dish["tags"]:
        score += 0.35
        reasons.append(f"Fits your {answers['craving']} craving")
    else:
        # ❌ penalty if craving does not match
        score -= 0.15

    # 2️⃣ Situation — STRONG signal
    if answers["situation"] in dish.get("contexts", []):
        readable = answers["situation"].replace("_", " ")
        score += 0.30
        reasons.append(f"Good choice for {readable}")
    else:
        # ❌ penalty if situation does not match
        score -= 0.10

    # 3️⃣ City bias — SOFT signal (strongest only)
    bias_scores = [city_bias.get(tag, 0) for tag in dish["tags"]]
    if bias_scores:
        score += max(bias_scores) * 0.20

    # 4️⃣ Popularity — VERY soft signal
    score += dish.get("popularity", 0.5) * 0.10

    # 5️⃣ Time of day — contextual bonus
    time_bucket = get_time_bucket()
    if time_bucket in dish.get("time_suitable", []):
        score += 0.15
        reasons.append(f"Works well for {time_bucket} time")

    # 6️⃣ Day type — weekend indulgence
    if get_day_type() == "weekend" and "indulgent" in dish["tags"]:
        score += 0.10
        reasons.append("Nice indulgent option for the weekend")

    # 7️⃣ Festival — rare but powerful
    festival = get_festival()
    if festival and festival in dish.get("festival_special", []):
        score += 0.20
        reasons.append(f"Popular choice for {festival}")

    # -------------------------------
    # Final cleanup
    # -------------------------------

    # Clamp score to [0, 1]
    score = round(min(max(score, 0.0), 1.0), 3)

    # Keep reasons short (top 3 only)
    reasons = reasons[:3]

    return score, reasons
