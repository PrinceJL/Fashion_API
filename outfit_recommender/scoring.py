from collections import Counter, defaultdict

def score_outfit(attributes: dict, categories: list, score_map: dict, attr_weights=None) -> tuple:
    """
    Scores an outfit for each category (style/body shape/occasion/season).
    """
    if attr_weights is None:
        attr_weights = defaultdict(lambda: 1.0)
    cat_scores = Counter()
    details = {}
    for cat in categories:
        total = 0
        breakdown = {}
        for attr, value in attributes.items():
            if attr not in score_map:
                continue
            scores_map = score_map[attr].get(value, {})
            score = scores_map.get(cat, 0)
            weight = attr_weights[attr]
            breakdown[attr] = round(score * weight, 2)
            total += score * weight
        cat_scores[cat] = total
        details[cat] = breakdown
    return dict(cat_scores), details