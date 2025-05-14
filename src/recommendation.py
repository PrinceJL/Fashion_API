import pandas as pd

class FashionRecommender:
    def __init__(self, csv_url):
        self.df = pd.read_csv(csv_url)

        # Keep image_label for gender filtering
        self.df['gender'] = self.df['image_label'].apply(lambda x: 'MEN' if x.startswith('MEN') else 'WOMEN')
        
        # One-hot encode fabric and pattern
        self.df = pd.get_dummies(self.df.drop(columns=['image_label']), columns=[
            'fabric_upper', 'fabric_lower', 'fabric_outer', 
            'pattern_upper', 'pattern_lower', 'pattern_outer'
        ], drop_first=True)

        self.style_columns = ['Casual', 'Formal', 'Trendy', 'Sporty', 'Streetwear', 
                              'Bohemian', 'Minimalist', 'Elegant']
        self.shape_columns = ['Hourglass', 'Triangle', 'Inverted Triangle', 'Rectangle', 'Oval']

    def recommend(self, styles=[], shapes=[], gender=None, top_k=5):
        df = self.df.copy()

        if gender in ['MEN', 'WOMEN']:
            df = df[df['gender'] == gender]

        if not styles and not shapes:
            return []

        score_cols = []
        if styles:
            score_cols += [col for col in styles if col in self.style_columns]
        if shapes:
            score_cols += [col for col in shapes if col in self.shape_columns]

        df["match_score"] = df[score_cols].sum(axis=1)
        top_matches = df.sort_values("match_score", ascending=False).head(top_k)

        base_cols = ['image_url', 'gender', 'sleeve_length', 'lower_length', 'socks', 'hat', 
                     'glasses', 'neckwear', 'wrist_wear', 'ring', 'waist_acc', 
                     'neckline', 'outer', 'covers_navel']
        fabric_pattern_cols = [col for col in df.columns if col.startswith(('fabric_', 'pattern_'))]

        return top_matches[base_cols + fabric_pattern_cols].to_dict(orient="records")
