import pandas as pd
import re
from src.scoring_engine import ScoringEngine


class RecommendationEngine:
    def __init__(self, scoring_engine: ScoringEngine, clothing_csv_url: str):
        """
        Initialize the Recommendation Engine with a scoring engine and clothing dataset.

        Args:
        - scoring_engine (ScoringEngine): Instance of ScoringEngine to compute scores.
        - clothing_csv_url (str): URL to the clothing data CSV file.
        """
        self.scoring_engine = scoring_engine
        self.clothing_csv_url = clothing_csv_url
        self.df_clothing = self._load_clothing_data()

    def _load_clothing_data(self):
        """
        Load the clothing dataset from the provided URL.

        Returns:
        - pd.DataFrame: Loaded clothing dataset.
        """
        return pd.read_csv(self.clothing_csv_url)

    def recommend(self, attributes: dict, body_shape: str, style: str, top_k: int, gender: str):
        """
        Recommend the top `k` clothing items based on the provided attributes, body shape, and style.

        Args:
        - attributes (dict): Numeric attributes (fabric, pattern, etc.).
        - body_shape (str): The user's body shape (e.g., 'Hourglass').
        - style (str): The selected style preference.
        - top_k (int): Number of top recommendations to return.
        - gender (str): Gender of the person (either 'men' or 'women').

        Returns:
        - list: Top `k` recommendations (each recommendation is a dict).
        """
        # Step 1: Compute fashion scores using ScoringEngine
        fashion_scores = self.scoring_engine.compute_scores(attributes)

        # Step 2: Ensure the requested style is valid
        if style not in fashion_scores:
            raise ValueError(f"Invalid style: {style}. Available styles are {list(fashion_scores.keys())}.")

        # Step 3: Filter the dataset for the user's gender using exact word match
        gender_pattern = rf"\b{gender.lower()}\b"  # Use word boundary to match 'men' or 'women' exactly
        filtered_df = self.df_clothing[self.df_clothing['image_label'].str.contains(gender_pattern, flags=re.IGNORECASE, regex=True)]

        if filtered_df.empty:
            raise ValueError(f"No clothing items found for gender: {gender}")

        # Step 4: Sort by body shape score and style score
        filtered_df['combined_score'] = filtered_df[body_shape] + filtered_df[style]
        filtered_df = filtered_df.sort_values(by='combined_score', ascending=False)

        # Step 5: Get the top `k` recommendations
        recommendations = filtered_df.head(top_k).to_dict('records')

        return recommendations