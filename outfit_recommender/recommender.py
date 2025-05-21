from .scoring import score_outfit
from .nlp_prompt_parser import parse_prompt

def recommend_best_combined(
    outfits,
    prompt,
    style_score_map,
    bodyshape_score_map,
    attr_weights=None,
    topk=3,
    style=None,
    body_shape=None,
    season=None,
    occasion=None,
    features=None,
):
    # If explicit style/body_shape/season/occasion/features provided, use them. Otherwise parse from prompt.
    if not (style and body_shape and season and occasion and features):
        parsed = parse_prompt(prompt)
        style = style or parsed["style"] or "Trendy"
        body_shape = body_shape or "Hourglass"
        season = season or parsed["season"]
        occasion = occasion or parsed["occasion"]
        features = features or parsed["features"]

    scored = []
    for outfit in outfits:
        style_scores, _ = score_outfit(outfit, [style], style_score_map, attr_weights)
        style_score = list(style_scores.values())[0] if style_scores else 0
        bs_scores, _ = score_outfit(outfit, [body_shape], bodyshape_score_map, attr_weights)
        bs_score = list(bs_scores.values())[0] if bs_scores else 0
        combined_score = style_score + bs_score
        # Feature filter — must match all features if specified
        if features:
            matches_all = all(
                any(v in str(attr_val).lower() for attr_val in outfit.values())
                for v in features.values()
            )
            if not matches_all:
                continue
        scored.append({
            'outfit': outfit,
            'score': combined_score,
            'style_score': style_score,
            'bodyshape_score': bs_score,
            'style': style,
            'body_shape': body_shape,
            'occasion': occasion,
            'season': season,
            'features': features
        })
    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:topk]