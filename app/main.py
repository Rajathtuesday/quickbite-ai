from fastapi import FastAPI, Query
from app.models import MenuUploadRequest, RecommendRequest, FeedbackRequest
from app.data import DISHES
from app.ml_scoring import ml_score_dish
from app.logger import log_recommendation
from app.feedback_logger import log_feedback
from app.menu_store import save_menu, load_menu
from pydantic import BaseModel
from typing import List


app = FastAPI(title="QuickBite Revenue AI", version="2.1")




@app.get("/")
def health():
    return {"status": "ok"}



@app.post("/v1/recommend")
def recommend(
    req: RecommendRequest,
    mode: str = Query("profit", enum=["profit", "click"])
):


    menu = load_menu(req.restaurant_id)

    if not menu:
        return {"error": "No menu found for this restaurant."}
    results = []
    for dish in menu:


        # Constraints
        if "veg_only" in req.answers.constraints and "veg" not in dish["tags"]:
            continue

        if "under_250" in req.answers.constraints and dish["price"] > 250:
            continue

        # ML probability
        prob = ml_score_dish(
            city=req.city,
            situation=req.answers.situation,
            craving=req.answers.craving,
            dish=dish
        )


        margin = dish["margin"]
        expected_profit = prob * margin

        # Mode-based scoring
        if mode == "click":
            final_score = prob
            reason = "Optimized for click probability"
        else:
            final_score = expected_profit
            reason = "Optimized for expected profit"

        results.append({
            "dish_id": dish["dish_id"],
            "name": dish["name"],
            "score": round(final_score, 3),
            "why": [reason]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    top_picks = results[:3]

    log_recommendation(req, top_picks)

    return {
        "mode": mode,
        "top_picks": top_picks,
        "decision_time_estimate_sec": 35
    }


@app.post("/v1/feedback")
def feedback(req: FeedbackRequest):

    log_feedback(
        restaurant_id=req.restaurant_id,
        session_id=req.session_id,
        dish_id=req.dish_id,
        action=req.action
    )

    return {"status": "feedback recorded"}


@app.post("/v1/upload_menu")
def upload_menu(req: MenuUploadRequest):

    menu_data = [dish.dict() for dish in req.menu]

    save_menu(req.restaurant_id, menu_data)

    return {
        "status": "menu uploaded",
        "restaurant_id": req.restaurant_id,
        "total_items": len(menu_data)
    }
    