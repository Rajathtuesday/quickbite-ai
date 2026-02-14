from pydantic import BaseModel
from typing import List



class Answers(BaseModel):
    situation: str
    craving: str
    constraints: List[str] = []


class RecommendRequest(BaseModel):
    restaurant_id: str
    city: str
    session_id: str
    answers: Answers


class FeedbackRequest(BaseModel):
    restaurant_id: str
    session_id: str
    dish_id: str
    action: str  # click or order



class DishUpload(BaseModel):
    dish_id: str
    name: str
    price: float
    margin: float
    tags: List[str]
    popularity: float


class MenuUploadRequest(BaseModel):
    restaurant_id: str
    menu: List[DishUpload]




class OrderRequest(BaseModel):
    restaurant_id: str
    table_id: str
    session_id: str
    dish_id: str
