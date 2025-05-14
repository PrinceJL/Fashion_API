import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

class FashionRecommender:
    def __init__(self, csv_url):
        self.df = pd.read_csv(csv_url)

        # Gender inference
        self.df['gender'] = self.df['image_label'].apply(lambda x: 'MEN' if x.startswith('MEN') else 'WOMEN')

        # One-hot encode fabrics and patterns
        self.df = pd.get_dummies(self.df.drop(columns=['image_label']), columns=[
            'fabric_upper', 'fabric_lower', 'fabric_outer',
            'pattern_upper', 'pattern_lower', 'pattern_outer'
        ], drop_first=True)

        # Define style and shape columns
        self.style_columns = ['Casual', 'Formal', 'Trendy', 'Sporty', 'Streetwear', 
                              'Bohemian', 'Minimalist', 'Elegant']
        self.shape_columns = ['Hourglass', 'Triangle', 'Inverted Triangle', 'Rectangle', 'Oval']

        # Feature columns include base attributes, fabric/pattern, and body shape scores
        self.base_cols = ['sleeve_length', 'lower_length', 'socks', 'hat', 'glasses',
                          'neckwear', 'wrist_wear', 'ring', 'waist_acc', 'neckline',
                          'outer', 'covers_navel']
        self.fabric_pattern_cols = [col for col in self.df.columns if col.startswith(('fabric_', 'pattern_'))]
        self.feature_cols = self.base_cols + self.fabric_pattern_cols + self.shape_columns

        # Placeholder for trained models
        self.models = {}

    def train_models(self):
        """Train models for each style score."""
        for style in self.style_columns:
            X = self.df[self.feature_cols]
            y = self.df[style]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            print(f"Trained model for {style} — R²: {r2_score(y_test, y_pred):.2f}, MAE: {mean_absolute_error(y_test, y_pred):.2f}")

            self.models[style] = model

    def calculate_body_shape_fit(self, item_row, user_shape_scores):
        """
        Calculate how well the item fits the user's body shape based on body shape scores.
        """
        fit_score = 0
        for shape, score in user_shape_scores.items():
            fit_score += item_row[shape] * score  # Multiply each attribute with corresponding score
        return fit_score

    def recommend(self, user_styles=[], user_shape_scores=None, gender=None, top_k=5):
        """
        Recommend clothing items based on user style preferences and body shape fit.
        """
        df = self.df.copy()

        if gender in ['MEN', 'WOMEN']:
            df = df[df['gender'] == gender]

        if not user_styles:
            return []

        # Predict preference scores for each style and average them
        X = df[self.feature_cols]
        df['predicted_score'] = 0
        for style in user_styles:
            if style in self.models:
                df['predicted_score'] += self.models[style].predict(X)
        df['predicted_score'] /= len(user_styles)

        # Personalize recommendations based on body shape fit scores
        if user_shape_scores:
            df['body_shape_fit'] = df.apply(lambda row: self.calculate_body_shape_fit(row, user_shape_scores), axis=1)
            df['personalized_score'] = df['predicted_score'] * df['body_shape_fit']
        else:
            df['personalized_score'] = df['predicted_score']

        # Sort and return top recommendations
        top_matches = df.sort_values('personalized_score', ascending=False).head(top_k)

        return top_matches[['image_url', 'gender'] + self.base_cols + self.fabric_pattern_cols].to_dict(orient='records')
