import pandas as pd
from app.ml_model import get_model
from app.data import DISHES

dish_lookup = {d["dish_id"]: d for d in DISHES}

def ml_score_dish(city, situation, craving, dish_id):

    model = get_model()

    dish = dish_lookup[dish_id]
    tags = dish["tags"]

    row = pd.DataFrame([{
        "city": city,
        "context_combo": situation + "_" + craving,

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
    }])

    prob = model.predict_proba(row)[0][1]
    return round(float(prob), 3)
