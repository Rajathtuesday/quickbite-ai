from fastapi import FastAPI, Query
from app.models import MenuUploadRequest, RecommendRequest, FeedbackRequest
from app.data import DISHES
from app.ml_scoring import ml_score_dish
from app.logger import log_recommendation
from app.feedback_logger import log_feedback
from app.menu_store import save_menu, load_menu
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from datetime import datetime
import json
import os 

app = FastAPI(title="QuickBite Revenue AI", version="2.2")




@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}


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
    
    





ORDERS_FILE = "logs/orders.jsonl"
os.makedirs("logs", exist_ok=True)


@app.post("/v1/order")
def place_order(payload: dict):

    restaurant_id = payload["restaurant_id"]
    table_id = payload["table_id"]
    dish_id = payload["dish_id"]
    session_id = payload["session_id"]

    order_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "restaurant_id": restaurant_id,
        "table_id": table_id,
        "dish_id": dish_id,
        "session_id": session_id
    }

    with open(ORDERS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(order_entry) + "\n")

    # WhatsApp number (for pilot)
    whatsapp_number = "917899814912"  # replace with real number

    message = f"Table {table_id} wants to order {dish_id}"
    whatsapp_link = f"https://wa.me/{whatsapp_number}?text={message}"

    return {
        "status": "order_logged",
        "whatsapp_url": whatsapp_link
    }


@app.get("/debug/orders")
def debug_orders():
    try:
        with open("logs/orders.jsonl", "r", encoding="utf-8") as f:
            lines = f.readlines()
            return {
                "total_orders": len(lines),
                "last_5": [json.loads(l) for l in lines[-5:]]
            }
    except FileNotFoundError:
        return {"total_orders": 0, "last_5": []}
