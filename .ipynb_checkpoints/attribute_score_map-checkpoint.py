import csv
import requests
from collections import defaultdict, Counter

# --- CONFIGURATION ---

# 1. Attribute code to value mappings (from your earlier description)
ATTRIBUTE_CODE_MAPS = {
    "sleeve_length": {
        "0": "Sleeveless", "1": "Short Sleeve", "2": "Medium Sleeve", "3": "Long Sleeve", "4": "Not Long Sleeve", "5": "NA"
    },
    "lower_length": {
        "0": "Three-Point", "1": "Medium Short", "2": "Three-Quarter", "3": "Long", "4": "NA"
    },
    "socks": {
        "0": "No", "1": "Socks", "2": "Leggings", "3": "NA"
    },
    "hat": {
        "0": "No", "1": "Yes", "2": "NA"
    },
    "glasses": {
        "0": "No", "1": "Eyeglasses", "2": "Sunglasses", "3": "Glasses in Hand or Clothes", "4": "NA"
    },
    "neckwear": {
        "0": "No", "1": "Yes", "2": "NA"
    },
    "wrist_wear": {
        "0": "No", "1": "Yes", "2": "NA"
    },
    "ring": {
        "0": "No", "1": "Yes", "2": "NA"
    },
    "waist_acc": {
        "0": "No", "1": "Belt", "2": "Clothing", "3": "Hidden", "4": "NA"
    },
    "neckline": {
        "0": "V-shape", "1": "Square", "2": "Round", "3": "Standing", "4": "Lapel", "5": "Suspenders", "6": "NA"
    },
    "outer": {
        "0": "Cardigan", "1": "No", "2": "NA"
    },
    "covers_navel": {
        "0": "No", "1": "Yes", "2": "NA"
    },
    "fabric_upper": {
        "0": "denim", "1": "cotton", "2": "leather", "3": "furry", "4": "knitted", "5": "chiffon", "6": "other", "7": "NA"
    },
    "fabric_lower": {
        "0": "denim", "1": "cotton", "2": "leather", "3": "furry", "4": "knitted", "5": "chiffon", "6": "other", "7": "NA"
    },
    "fabric_outer": {
        "0": "denim", "1": "cotton", "2": "leather", "3": "furry", "4": "knitted", "5": "chiffon", "6": "other", "7": "NA"
    },
    "pattern_upper": {
        "0": "Floral", "1": "Graphic", "2": "Striped", "3": "Pure Color", "4": "Lattice", "5": "Other", "6": "Color Block", "7": "NA"
    },
    "pattern_lower": {
        "0": "Floral", "1": "Graphic", "2": "Striped", "3": "Pure Color", "4": "Lattice", "5": "Other", "6": "Color Block", "7": "NA"
    },
    "pattern_outer": {
        "0": "Floral", "1": "Graphic", "2": "Striped", "3": "Pure Color", "4": "Lattice", "5": "Other", "6": "Color Block", "7": "NA"
    }
}

STYLE_NAMES = ['Formal', 'Casual', 'Trendy', 'Bohemian', 'Minimalist', 'Streetwear', 'Elegant']

# --- 2. URLs to the mapping and dataset ---
ATTRIBUTE_SCORE_CSV_URL = "https://docs.google.com/spreadsheets/d/1Zx66-QAVjLJjUdP3rVfE2nbCWVQwkVv0IKaLRO7EH9M/export?format=csv&gid=0"
OUTFIT_DATASET_CSV_URL = "https://docs.google.com/spreadsheets/d/1Uj88haHGZCsSQW5c27SDcJyvcBPlLJGP8WKZvw2dWqg/export?format=csv&gid=1320449891"

# --- 3. Default attribute weights (can be learned/tuned with data science) ---
DEFAULT_ATTR_WEIGHTS = defaultdict(lambda: 1.0)

# --- FUNCTION TO LOAD ATTRIBUTE-SCORE MAP FROM GOOGLE SHEETS ---
def load_attribute_score_map(csv_url):
    response = requests.get(csv_url)
    response.raise_for_status()
    lines = response.content.decode('utf-8').splitlines()
    reader = csv.DictReader(lines)
    mapping = defaultdict(lambda: defaultdict(dict))
    for row in reader:
        attr = row['Classification'].strip()
        value = row['Attribute Name'].strip()
        for style in STYLE_NAMES:
            score_raw = row.get(style, "").strip()
            try:
                score = int(score_raw)
            except Exception:
                score = 0
            mapping[attr][value][style] = score
    return mapping

# --- FUNCTION TO LOAD OUTFIT DATASET ---
def load_outfit_dataset(csv_url):
    response = requests.get(csv_url)
    response.raise_for_status()
    lines = response.content.decode('utf-8').splitlines()
    reader = csv.DictReader(lines, delimiter=',')
    dataset = []
    for row in reader:
        mapped = {}
        for attr in ATTRIBUTE_CODE_MAPS:
            code = row.get(attr, None)
            mapped[attr] = ATTRIBUTE_CODE_MAPS[attr].get(code, "NA") if code is not None else "NA"
        mapped['image_label'] = row.get('image_label', '')
        mapped['image_url'] = row.get('image_url', '')
        dataset.append(mapped)
    return dataset

# --- FUNCTION TO PARSE USER PROMPT INTO STYLES/KEYWORDS ---
def parse_user_prompt(prompt):
    styles = []
    keywords = []
    prompt_lower = prompt.lower()
    for s in STYLE_NAMES:
        if s.lower() in prompt_lower:
            styles.append(s)
    for k in ['short sleeve', 'long sleeve', 'cotton', 'denim', 'summer', 'belt', 'v-shape', 'knitted', 'floral', 'chiffon']:
        if k in prompt_lower:
            keywords.append(k)
    return styles, keywords

# --- AI-DRIVEN RULE-BASED SCORING FUNCTION ---
def score_outfit(attributes, styles, score_map, attr_weights=None):
    if attr_weights is None:
        attr_weights = DEFAULT_ATTR_WEIGHTS
    style_scores = Counter()
    details = {}
    for style in styles:
        total = 0
        breakdown = {}
        for attr, value in attributes.items():
            if attr not in score_map: continue
            style_scores_map = score_map[attr].get(value, {})
            score = style_scores_map.get(style, 0)
            weight = attr_weights[attr]
            breakdown[attr] = round(score * weight, 2)
            total += score * weight
        style_scores[style] = total
        details[style] = breakdown
    return dict(style_scores), details

def recommend_best(outfits, prompt, score_map, attr_weights=None, topk=3):
    styles, keywords = parse_user_prompt(prompt)
    if not styles:
        styles = ['Trendy'] # Default/fallback
    scored = []
    for outfit in outfits:
        scores, details = score_outfit(outfit, styles, score_map, attr_weights)
        avg_score = sum(scores.values()) / len(scores)
        # Optional: filter by keywords
        if keywords:
            matched = any(any(k in str(v).lower() for v in outfit.values()) for k in keywords)
            if not matched:
                continue
        scored.append({
            'outfit': outfit,
            'score': avg_score,
            'details': details,
            'styles': styles
        })
    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:topk]

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("Loading attribute scoring matrix...")
    score_map = load_attribute_score_map(ATTRIBUTE_SCORE_CSV_URL)
    print("Loading outfit dataset...")
    outfits = load_outfit_dataset(OUTFIT_DATASET_CSV_URL)
    print(f"Loaded {len(outfits)} outfits.")

    # Example: user prompt
    user_prompt = input("Enter your style prompt (e.g. 'I want something elegant and casual for summer'): ")
    results = recommend_best(outfits, user_prompt, score_map, DEFAULT_ATTR_WEIGHTS, topk=3)

    print("\nTop Recommendations:")
    for idx, res in enumerate(results, 1):
        print(f"\n#{idx}:")
        print("Image:", res['outfit']['image_label'])
        print("Image URL:", res['outfit']['image_url'])
        print("Attributes:", {k:v for k,v in res['outfit'].items() if k not in ['image_label', 'image_url']})
        print("Score:", res['score'])
        print("Styles:", res['styles'])
        print("Score details per attribute:", res['details'])