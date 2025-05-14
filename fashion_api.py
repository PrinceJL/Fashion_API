from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from src.recommendation import FashionRecommender

app = FastAPI()

recommender = FashionRecommender(
    "https://docs.google.com/spreadsheets/d/1Uj88haHGZCsSQW5c27SDcJyvcBPlLJGP8WKZvw2dWqg/export?format=csv&gid=1320449891"
)

class RecommendationRequest(BaseModel):
    styles: Optional[List[str]] = []
    shapes: Optional[List[str]] = []
    gender: Optional[str] = None
    top_k: Optional[int] = 5

@app.post("/recommend")
def recommend_clothes(request: RecommendationRequest):
    results = recommender.recommend(
        styles=request.styles,
        shapes=request.shapes,
        gender=request.gender,
        top_k=request.top_k
    )
    return {"recommendations": results}
