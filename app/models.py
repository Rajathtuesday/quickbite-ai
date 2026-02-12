from pydantic import BaseModel
from typing import List


class Answers(BaseModel):
    situation: str
    craving: str
    constraints: List[str] = []


class RecommendRequest(BaseModel):
    city: str
    session_id: str
    answers: Answers


class FeedbackRequest(BaseModel):
    session_id: str
    dish_id: str
    action: str  # "click" or "order"
