from app.ml_model import get_model
import pandas as pd

def ml_score_dish(city, situation, craving, dish):

    model = get_model()

    context_combo = situation + "_" + craving
    tags = dish["tags"]

    row = pd.DataFrame([{
        "city": city,
        "context_combo": context_combo,
        "is_spicy": int("spicy" in tags),
        "is_creamy": int("creamy" in tags),
        "is_sweet": int("sweet" in tags),
        "is_fried": int("fried" in tags),
        "is_healthy": int("healthy" in tags),
        "is_indulgent": int("indulgent" in tags),
        "is_south_indian": int("south_indian" in tags),
        "is_north_indian": int("north_indian" in tags),
        "is_street_food": int("street_food" in tags),
        "popularity": dish.get("popularity", 0.5),
        "price_bucket": int(dish["price"] // 100),
    }])

    prob = model.predict_proba(row)[0][1]
    return float(prob)
