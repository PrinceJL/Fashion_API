import csv
import requests
from collections import defaultdict
from .attribute_mapping import ATTRIBUTE_CODE_MAPS

def infer_gender_from_label(image_label):
    label = image_label.lower()
    if label.startswith("men"):
        return "male"
    elif label.startswith("women"):
        return "female"
    return "unisex"

def load_score_map(csv_url: str, col_names: list) -> dict:
    """Loads a scoring matrix from a Google Sheets CSV URL."""
    response = requests.get(csv_url)
    response.raise_for_status()
    lines = response.content.decode('utf-8').splitlines()
    reader = csv.DictReader(lines)
    mapping = defaultdict(lambda: defaultdict(dict))
    for row in reader:
        attr = row['Classification'].strip()
        value = row['Attribute Name'].strip()
        for col in col_names:
            score_raw = row.get(col, "").strip()
            try:
                score = int(score_raw)
            except Exception:
                score = 0
            mapping[attr][value][col] = score
    return mapping

def load_outfit_dataset(csv_url: str) -> list:
    """Loads the outfit dataset and decodes coded attributes. Infers gender from file name."""
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
        mapped['gender'] = infer_gender_from_label(mapped['image_label'])
        dataset.append(mapped)
    return dataset