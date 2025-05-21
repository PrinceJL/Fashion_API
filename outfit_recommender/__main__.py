"""
Main command-line interface for AI-Driven Outfit Recommender using full dataset and AI prompt parsing.
"""

from outfit_recommender.data_loader import load_score_map, load_outfit_dataset
from outfit_recommender.attribute_mapping import STYLE_NAMES, BODYSHAPE_NAMES
from outfit_recommender.recommender import recommend_best_combined
from collections import defaultdict

STYLE_SCORE_CSV_URL = "https://docs.google.com/spreadsheets/d/1Zx66-QAVjLJjUdP3rVfE2nbCWVQwkVv0IKaLRO7EH9M/export?format=csv&gid=0"
BODYSHAPE_SCORE_CSV_URL = "https://docs.google.com/spreadsheets/d/1Zx66-QAVjLJjUdP3rVfE2nbCWVQwkVv0IKaLRO7EH9M/export?format=csv&gid=28283272"
OUTFIT_DATASET_CSV_URL = "https://docs.google.com/spreadsheets/d/1Uj88haHGZCsSQW5c27SDcJyvcBPlLJGP8WKZvw2dWqg/export?format=csv&gid=1320449891"

DEFAULT_ATTR_WEIGHTS = defaultdict(lambda: 1.0)

def print_recommendations(results):
    for idx, res in enumerate(results, 1):
        print(f"\n#{idx}:")
        print("Gender:", res['outfit']['gender'])
        print("Image:", res['outfit']['image_label'])
        print("Image URL:", res['outfit']['image_url'])
        print("Attributes:", {k:v for k,v in res['outfit'].items() if k not in ['image_label', 'image_url', 'gender']})
        print("Total Score:", res['score'])
        print(f"  Style Score: {res['style_score']}  | Style: {res['style']}")
        print(f"  Body Shape Score: {res['bodyshape_score']}  | Body Shape: {res['body_shape']}")
        if res['occasion'] or res['season']:
            print(f"Occasion: {res['occasion']}  | Season: {res['season']}")
        if res['features']:
            print("Features matched:", res['features'])

def main():
    print("Loading style scoring matrix...")
    style_score_map = load_score_map(STYLE_SCORE_CSV_URL, STYLE_NAMES)
    print("Loading body shape scoring matrix...")
    bodyshape_score_map = load_score_map(BODYSHAPE_SCORE_CSV_URL, BODYSHAPE_NAMES)
    print("Loading outfit dataset...")
    outfits = load_outfit_dataset(OUTFIT_DATASET_CSV_URL)
    print(f"Loaded {len(outfits)} outfits.")

    print("\nWelcome to the AI-Driven Outfit Recommender!")
    gender = input("Enter gender (male/female): ").strip().lower()
    body_shape = input(f"Enter body shape ({', '.join(BODYSHAPE_NAMES)}): ").strip().title()
    user_prompt = input("Describe your style/season/occasion/features: ")

    # Only use outfits matching gender
    filtered_outfits = [o for o in outfits if o['gender'] == gender or o['gender'] == "unisex"]

    results = recommend_best_combined(
        filtered_outfits,
        user_prompt,
        style_score_map,
        bodyshape_score_map,
        DEFAULT_ATTR_WEIGHTS,
        topk=3,
        style=None,
        body_shape=body_shape,  # use explicit input
    )
    print("\nTop Recommendations:")
    print_recommendations(results)

if __name__ == "__main__":
    main()