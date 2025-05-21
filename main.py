from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from outfit_recommender.data_loader import load_score_map, load_outfit_dataset
from outfit_recommender.attribute_mapping import STYLE_NAMES, BODYSHAPE_NAMES
from outfit_recommender.nlp_prompt_parser import parse_prompt
from outfit_recommender.recommender import recommend_best_combined
from collections import defaultdict

app = FastAPI(
    title="AI-Driven Outfit Recommender API",
    description="Recommend outfits based on user profile and natural language prompt.",
    version="1.0.0"
)

# Load at startup
STYLE_SCORE_CSV_URL = "https://docs.google.com/spreadsheets/d/1Zx66-QAVjLJjUdP3rVfE2nbCWVQwkVv0IKaLRO7EH9M/export?format=csv&gid=0"
BODYSHAPE_SCORE_CSV_URL = "https://docs.google.com/spreadsheets/d/1Zx66-QAVjLJjUdP3rVfE2nbCWVQwkVv0IKaLRO7EH9M/export?format=csv&gid=28283272"
OUTFIT_DATASET_CSV_URL = "https://docs.google.com/spreadsheets/d/1Uj88haHGZCsSQW5c27SDcJyvcBPlLJGP8WKZvw2dWqg/export?format=csv&gid=1320449891"

DEFAULT_ATTR_WEIGHTS = defaultdict(lambda: 1.0)

# Preload data
@app.on_event("startup")
def load_data():
    global style_score_map, bodyshape_score_map, outfits
    style_score_map = load_score_map(STYLE_SCORE_CSV_URL, STYLE_NAMES)
    bodyshape_score_map = load_score_map(BODYSHAPE_SCORE_CSV_URL, BODYSHAPE_NAMES)
    outfits = load_outfit_dataset(OUTFIT_DATASET_CSV_URL)

class RecommendationRequest(BaseModel):
    gender: str = Field(..., example="male")
    body_shape: str = Field(..., example="Hourglass")
    prompt: str = Field(..., example="I want a formal outfit for a summer wedding, prefer short sleeves and cotton")
    topk: int = Field(3, ge=1, le=10, description="Number of recommendations to return")

class OutfitResponse(BaseModel):
    gender: str
    image_label: str
    image_url: str
    attributes: Dict[str, Any]
    total_score: int
    style_score: int
    bodyshape_score: int

class RecommendationResponse(BaseModel):
    recommendations: List[OutfitResponse]

@app.post("/recommend", response_model=RecommendationResponse)
def recommend_outfits(request: RecommendationRequest):
    # Filter outfits by gender
    filtered = [o for o in outfits if o['gender'] == request.gender or o['gender'] == "unisex"]
    parsed = parse_prompt(request.prompt)
    style = parsed['style'] or "Casual"
    features = parsed['features']
    results = recommend_best_combined(
        filtered,
        request.prompt,
        style_score_map,
        bodyshape_score_map,
        DEFAULT_ATTR_WEIGHTS,
        topk=request.topk,
        style=style,
        body_shape=request.body_shape,
        features=features
    )
    resp = [
        OutfitResponse(
            gender=res['outfit']['gender'],
            image_label=res['outfit']['image_label'],
            image_url=res['outfit']['image_url'],
            attributes={k: v for k, v in res['outfit'].items() if k not in ['image_label', 'image_url', 'gender']},
            total_score=res['score'],
            style_score=res['style_score'],
            bodyshape_score=res['bodyshape_score']
        )
        for res in results
    ]
    return RecommendationResponse(recommendations=resp)