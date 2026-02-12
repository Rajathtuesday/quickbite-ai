from fastapi import FastAPI
from app.models import RecommendRequest
from app.data import BANGALORE_BIAS, DISHES
from app.logger import log_recommendation
from app.feedback_logger import log_feedback
from app.models import FeedbackRequest
from app.ml_scoring import ml_score_dish
from app.scoring import score_dish
from app.session_memory import boost_dish, get_boost

app = FastAPI(title="QuickBite AI", version="0.1.0")

@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/v1/recommend")
def recommend(req: RecommendRequest):
    results = []

    for dish in DISHES:

        # Hard constraints
        if "veg_only" in req.answers.constraints and "veg" not in dish["tags"]:
            continue
        if "under_250" in req.answers.constraints and dish["price"] > 250:
            continue

        # score = ml_score_dish(
        #     city=req.city,
        #     situation=req.answers.situation,
        #     craving=req.answers.craving,
        #     dish_id=dish["dish_id"]
        # )
        base_score = ml_score_dish(
        city=req.city,
        situation=req.answers.situation,
        craving=req.answers.craving,
        dish_id=dish["dish_id"]
    )

        boost = get_boost(req.session_id, dish["dish_id"])

        score = min(base_score + boost, 1.0)



        results.append({
            "dish_id": dish["dish_id"],
            "name": dish["name"],
            "score": score,
            "why": ["Recommended based on similar past behavior"]
        })

    # Sort highest score first
    results.sort(key=lambda x: x["score"], reverse=True)

    top_picks = results[:3]

    log_recommendation(req, top_picks)

    return {
        "top_picks": top_picks,
        "decision_time_estimate_sec": 40
    }


@app.post("/v1/feedback")
def feedback(req: FeedbackRequest):
    if req.action == "click":
        boost_dish(req.session_id, req.dish_id)
    
    log_feedback(
        session_id=req.session_id,
        dish_id=req.dish_id,
        action=req.action
    )
    return {"status": "feedback recorded"}
