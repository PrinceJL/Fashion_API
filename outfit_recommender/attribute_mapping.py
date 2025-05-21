"""
Attribute code-to-value mappings and valid category sets.
"""

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
BODYSHAPE_NAMES = ['Hourglass', 'Triangle', 'Inverted Triangle', 'Rectangle', 'Oval']
SEASON_NAMES = ['summer', 'winter', 'spring', 'fall', 'autumn', 'rainy', 'dry', 'hot', 'cold']
OCCASION_NAMES = [
    'wedding', 'party', 'interview', 'work', 'office', 'business', 'meeting',
    'holiday', 'vacation', 'date', 'sport', 'gym', 'ceremony', 'graduation', 'picnic'
]