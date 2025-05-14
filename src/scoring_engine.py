import pandas as pd
import numpy as np
from collections import defaultdict

class ScoringEngine:
    def __init__(self, score_csv_url, clothing_csv_url):
        """
        Initialize the ScoringEngine with URLs for the scoring matrix and clothing data.

        Args:
        - score_csv_url (str): URL to the scoring matrix CSV file.
        - clothing_csv_url (str): URL to the clothing data CSV file.
        """
        self.score_csv_url = score_csv_url
        self.clothing_csv_url = clothing_csv_url
        self.score_columns = ['Formal', 'Casual', 'Trendy', 'Bohemian', 'Minimalist', 'Streetwear', 'Elegant']
        self.attributes = [
            'shape', 'fabric', 'pattern'
        ]
        self.score_dict = self._load_scoring_matrix()

    def _load_scoring_matrix(self):
        """
        Load the scoring matrix into a nested dictionary for fast access.

        Returns:
        - dict: Nested dictionary of scores.
        """
        df_scores = pd.read_csv(self.score_csv_url)
        df_scores[self.score_columns] = df_scores[self.score_columns].apply(pd.to_numeric, errors='coerce') * 0.10

        score_dict = defaultdict(lambda: defaultdict(dict))
        grouped = df_scores.groupby('Classification')
        for classification, group in grouped:
            group = group.reset_index(drop=True)
            for idx, row in group.iterrows():
                for shape in self.score_columns:
                    score = row[shape]
                    if pd.notna(score):
                        score_dict[classification][idx][shape] = round(score, 1)
        return score_dict

    def compute_scores(self, attributes: dict):
        """
        Compute scores for all styles based on provided attributes.

        Args:
        - attributes (dict): Attributes (shape, fabric, pattern).

        Returns:
        - dict: Scores for each style.
        """
        scores = {shape: [] for shape in self.score_columns}

        for attr, val in attributes.items():
            if attr in self.attributes and pd.notna(val):
                try:
                    val = int(val)
                    for shape in self.score_columns:
                        score = self.score_dict[attr][val].get(shape)
                        if score is not None:
                            scores[shape].append(score)
                except (KeyError, ValueError):
                    continue  # Skip unknown attributes or non-integer values

        # Average scores
        averaged_scores = {
            shape: round(np.mean(score_list), 2) if score_list else 0.0
            for shape, score_list in scores.items()
        }
        return averaged_scores