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
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.db import get_connection
import json
import os
from app.db import init_db  
from fastapi.responses import FileResponse
from app.models import RecommendRequest, FeedbackRequest, OrderRequest


app = FastAPI(title="QuickBite Revenue AI", version="2.2")
templates = Jinja2Templates(directory="app/templates")



@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}

@app.on_event("startup")
def startup():
    init_db()

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
def place_order(req: OrderRequest):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders (restaurant_id, table_id, dish_id, session_id)
        VALUES (?, ?, ?, ?)
    """, (req.restaurant_id, req.table_id, req.dish_id, req.session_id))

    conn.commit()
    conn.close()

    whatsapp_url = f"https://wa.me/917899814912?text=Table {req.table_id} wants to order {req.dish_id}"

    return {
        "status": "order_logged",
        "whatsapp_url": whatsapp_url
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


@app.get("/menu", response_class=HTMLResponse)
def menu_page(request: Request, restaurant_id: str, table_id: str):

    return templates.TemplateResponse("menu.html", {
        "request": request,
        "restaurant_id": restaurant_id,
        "table_id": table_id
    })



@app.get("/debug/download_db")
def download_db():
    return FileResponse("database.db", media_type="application/octet-stream", filename="database.db")


@app.get("/owner/menu", response_class=HTMLResponse)
def owner_menu_page(request: Request):
    return templates.TemplateResponse("owner_menu.html", {"request": request})

@app.get("/menu", response_class=HTMLResponse)
def customer_menu(request: Request):
    return templates.TemplateResponse("customer_menu.html", {"request": request})
