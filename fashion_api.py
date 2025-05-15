from fastapi import FastAPI
from pydantic import BaseModel
from src.recommendation_engine import RecommendationEngine
from src.scoring_engine import ScoringEngine

# Initialize FastAPI
app = FastAPI()

# Initialize Engines
scoring_engine = ScoringEngine(
    score_csv_url="https://docs.google.com/spreadsheets/d/1Zx66-QAVjLJjUdP3rVfE2nbCWVQwkVv0IKaLRO7EH9M/export?format=csv&gid=0",
    clothing_csv_url="https://docs.google.com/spreadsheets/d/1Uj88haHGZCsSQW5c27SDcJyvcBPlLJGP8WKZvw2dWqg/export?format=csv&gid=1320449891"
)
recommendation_engine = RecommendationEngine(
    scoring_engine=scoring_engine,
    clothing_csv_url="https://docs.google.com/spreadsheets/d/1Uj88haHGZCsSQW5c27SDcJyvcBPlLJGP8WKZvw2dWqg/export?format=csv&gid=1320449891"
)

# Define Request Schema
class RecommendationRequest(BaseModel):
    attributes: dict  # Attributes (numeric values for shape, fabric, pattern, etc.)
    body_shape: str  # Body shape (e.g., 'Hourglass')
    prompt: str  # User's prompt (e.g., "I want a casual outfit with a denim jacket")
    top_k: int  # Number of top recommendations to return
    gender: str  # Gender (e.g., 'men', 'women')

@app.post("/recommend")
async def recommend_clothes(request: RecommendationRequest):
    """
    Recommend the top `k` clothing items based on the provided attributes, body shape, and prompt.

    Args:
    - request (RecommendationRequest): Request body containing attributes, body shape, prompt, top_k, and gender.

    Returns:
    - list: Top `k` recommendations.
    """
    recommendations = recommendation_engine.recommend(
        attributes=request.attributes,
        body_shape=request.body_shape,
        prompt=request.prompt,
        top_k=request.top_k,
        gender=request.gender
    )
    return recommendations