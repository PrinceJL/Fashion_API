from .scoring import score_outfit
from .nlp_prompt_parser import parse_prompt
from .soscoring import heuristic_season_score, heuristic_occasion_score

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
    # Parse prompt if not explicitly provided
    if not (style and body_shape and season and occasion and features):
        parsed = parse_prompt(prompt)
        style = style or parsed.get("style") or "Trendy"
        body_shape = body_shape or parsed.get("body_shape") or "Hourglass"
        season = season or parsed.get("season")
        occasion = occasion or parsed.get("occasion")
        features = features or parsed.get("features")

    scored = []
    for outfit in outfits:
        # --- Step 1: Style Matching ---
        style_scores, _ = score_outfit(outfit, [style], style_score_map, attr_weights)
        style_score = list(style_scores.values())[0] if style_scores else 0

        # If style match is too low, skip outfit early (hard rule)
        if style_score < 0.3:
            continue  # Outfit style mismatch too strong

        # --- Step 2: Body Shape Compatibility ---
        bs_scores, _ = score_outfit(outfit, [body_shape], bodyshape_score_map, attr_weights)
        bs_score = list(bs_scores.values())[0] if bs_scores else 0

        # Moderate penalty if body shape score is very low but don't exclude outright
        if bs_score < 0.2:
            bs_score *= 0.5  # Penalize but keep for diversity

        # --- Step 3: Season Suitability ---
        season_score = heuristic_season_score(outfit, season) if season else 0
        # Reward matching season moderately, penalize mismatch slightly
        if season_score < 0.1:
            season_score -= 0.1  # small penalty for season mismatch

        # --- Step 4: Occasion Relevance ---
        occasion_score = heuristic_occasion_score(outfit, occasion) if occasion else 0
        # Occasion is very important, scale by 1.5
        occasion_score *= 1.5

        # --- Step 5: Feature Precision ---
        feature_bonus = 0
        if features:
            # Calculate how many features matched
            total_features = len(features)
            matched_features = 0
            for key, val in features.items():
                val = val.lower()
                # Some features may be list, convert all to string lower for search
                outfit_vals = [str(v).lower() for v in outfit.values()]
                if any(val in ov for ov in outfit_vals):
                    matched_features += 1
            # Feature bonus proportional to matched ratio, scaled small
            feature_bonus = (matched_features / total_features) * 0.2

        # --- Step 6: Combine all scores with weights reflecting importance ---
        combined_score = (
            (style_score * 3.0) +       # style is most important
            (bs_score * 2.0) +          # body shape next
            (occasion_score * 2.5) +    # occasion very important
            (season_score * 1.5) +      # season moderate importance
            feature_bonus               # feature bonus small
        )

        scored.append({
            'outfit': outfit,
            'score': combined_score,
            'style_score': style_score,
            'bodyshape_score': bs_score,
            'season_score': season_score,
            'occasion_score': occasion_score,
            'feature_bonus': feature_bonus,
            'style': style,
            'body_shape': body_shape,
            'occasion': occasion,
            'season': season,
            'features': features
        })

    # Sort descending by combined score
    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:topk]
