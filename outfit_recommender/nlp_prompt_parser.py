import spacy
from .attribute_mapping import (
    STYLE_NAMES, BODYSHAPE_NAMES, SEASON_NAMES, OCCASION_NAMES
)

# Load spaCy (ensure 'en_core_web_sm' is installed)
nlp = spacy.load("en_core_web_sm")

FEATURE_KEYWORDS = {
    'sleeve': ['short sleeve', 'long sleeve', 'sleeveless', 'medium sleeve', 'not long sleeve'],
    'fabric': ['cotton', 'denim', 'leather', 'chiffon', 'knitted', 'furry'],
    'pattern': ['floral', 'graphic', 'striped', 'pure color', 'lattice', 'color block'],
}

def extract_entity(text, keywords_set):
    text = text.lower()
    for keyword in keywords_set:
        if keyword.lower() in text:
            return keyword
    return None

def extract_feature_entities(text, features_map):
    features = {}
    text = text.lower()
    for feature, vals in features_map.items():
        for val in vals:
            if val in text:
                features[feature] = val
    return features

def parse_prompt(prompt):
    doc = nlp(prompt)
    text = prompt.lower()
    # Find style
    style = extract_entity(text, STYLE_NAMES)
    # Find season
    season = extract_entity(text, SEASON_NAMES)
    # Find occasion
    occasion = extract_entity(text, OCCASION_NAMES)
    # Features (expandable)
    features = extract_feature_entities(text, FEATURE_KEYWORDS)
    # Fallback: NER for event/occasion if not captured
    if not occasion:
        for ent in doc.ents:
            if ent.label_ == "EVENT":
                occasion = ent.text
                break
    return {
        "style": style,
        "season": season,
        "occasion": occasion,
        "features": features
    }