from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import gdown
from src.recommendation import FashionRecommender

app = FastAPI()

# Function to download the model from Google Drive
def download_model_from_drive(file_id, output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)
    return output_path

# Load the Fashion Detect model from Google Drive
fashion_detect_model_path = "fashion_detect_model.keras"
drive_file_id = "1A1Ok9GY7y2G35_VsTVu9SICspzIJ_wIZ"
download_model_from_drive(drive_file_id, fashion_detect_model_path)
fashion_detect_model = load_model(fashion_detect_model_path)

# Initialize the FashionRecommender with CSV URL
recommender = FashionRecommender(
    "https://docs.google.com/spreadsheets/d/1Uj88haHGZCsSQW5c27SDcJyvcBPlLJGP8WKZvw2dWqg/export?format=csv&gid=1320449891"
)
recommender.train_models()

# Define the request body for recommendations
class RecommendationRequest(BaseModel):
    styles: Optional[List[str]] = []  # User style preferences
    body_shape_scores: Optional[dict] = {}  # User body shape scores
    gender: Optional[str] = None  # Gender for filtering
    top_k: Optional[int] = 5  # Number of recommendations to return

def preprocess_image(image: Image.Image):
    """
    Preprocess the image to match the input format of the Fashion Detect model.
    """
    image = image.resize((224, 224))  # Resize the image to the model's expected input size
    image_array = np.array(image) / 255.0  # Normalize pixel values
    return np.expand_dims(image_array, axis=0)  # Add batch dimension

@app.post("/recommend")
async def recommend_clothes(
    request: RecommendationRequest,
    file: UploadFile = File(...)
):
    """
    Endpoint for generating clothing recommendations based on user preferences
    and attributes detected from an uploaded image.
    """
    # Process uploaded image
    image = Image.open(file.file)
    input_data = preprocess_image(image)

    # Detect attributes using the Fashion Detect model
    predictions = fashion_detect_model.predict(input_data)

    # Format detected attributes (customize based on your model's output)
    detected_attributes = {
        "fabric": predictions[0][0],  # Example: Adjust indices based on model output
        "style": predictions[0][1],
        "color": predictions[0][2],
        "fit": predictions[0][3],
    }

    # Combine user-provided preferences with detected attributes
    combined_preferences = {
        "styles": request.styles,
        "body_shape_scores": request.body_shape_scores,
        "gender": request.gender,
        "detected_attributes": detected_attributes,
    }

    # Use the recommender to generate suggestions
    results = recommender.recommend(
        user_styles=combined_preferences["styles"],
        user_shape_scores=combined_preferences["body_shape_scores"],
        gender=combined_preferences["gender"],
        detected_attributes=combined_preferences["detected_attributes"],  # Integrate detected attributes
        top_k=request.top_k
    )

    return {"recommendations": results}