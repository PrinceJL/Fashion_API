import pandas as pd
from src.prompt_parser import parse_prompt
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

    def recommend(self, attributes: dict, body_shape: str, prompt: str, top_k: int, gender: str):
        """
        Recommend the top `k` clothing items based on the provided attributes, body shape, and prompt.

        Args:
        - attributes (dict): Numeric attributes (fabric, pattern, etc.).
        - body_shape (str): The user's body shape (e.g., 'Hourglass').
        - prompt (str): Natural language description of what the user wants to wear.
        - top_k (int): Number of top recommendations to return.
        - gender (str): Gender of the person (either 'men' or 'women').

        Returns:
        - list: Top `k` recommendations (each recommendation is a dict).
        """
        # Step 1: Parse the prompt
        parsed_prompt = parse_prompt(prompt)
        styles = parsed_prompt["styles"]
        clothing_types = parsed_prompt["clothing_types"]

        # Step 2: Compute fashion scores using ScoringEngine
        fashion_scores = self.scoring_engine.compute_scores(attributes)

        # Step 3: Filter the dataset for the user's gender
        filtered_df = self.df_clothing[self.df_clothing['image_label'].str.contains(gender.upper(), case=False)]

        if filtered_df.empty:
            raise ValueError(f"No clothing items found for gender: {gender}")

        # Step 4: Further filter by styles and clothing types
        style_columns = [style for style in styles if style in filtered_df.columns]
        if not style_columns:
            print(f"Warning: No exact matching styles found. Using fallback styles: {styles}")
            style_columns = ["casual"]  # Default fallback style

        filtered_df = filtered_df[filtered_df[style_columns].sum(axis=1) > 0]  # Keep rows matching any style
        if clothing_types:
            filtered_df = filtered_df[filtered_df['image_label'].str.contains('|'.join(clothing_types), case=False, regex=True)]

        # Step 5: Sort by body shape score and combined style score
        filtered_df['combined_score'] = filtered_df[body_shape] + filtered_df[style_columns].sum(axis=1)
        filtered_df = filtered_df.sort_values(by='combined_score', ascending=False)

        # Step 6: Get the top `k` recommendations
        recommendations = filtered_df.head(top_k).to_dict('records')

        return recommendations