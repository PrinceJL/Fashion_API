from typing import Dict, Any, Optional

def heuristic_season_score(outfit: Dict[str, Any], season: Optional[str]) -> float:
    """
    Assign heuristic scores to outfits based on the season.
    Args:
        outfit: dict of outfit attributes, keys are attribute names and values are codes or values
        season: target season string (e.g., 'summer', 'winter', 'spring', 'fall')
    Returns:
        float score based on matching season heuristics
    """
    if not season:
        return 0.0

    season = season.lower()
    score = 0.0

    fabric_upper = outfit.get("fabric_upper")
    fabric_lower = outfit.get("fabric_lower")
    fabric_outer = outfit.get("fabric_outer")

    pattern_upper = outfit.get("pattern_upper")
    pattern_lower = outfit.get("pattern_lower")
    pattern_outer = outfit.get("pattern_outer")

    sleeve_length = outfit.get("sleeve_length")
    outer = outfit.get("outer")
    covers_navel = outfit.get("covers_navel")

    # Summer: prefer light fabrics (cotton, chiffon), floral or pure colors, short sleeves, less outerwear
    if season in ["summer", "hot"]:
        if fabric_upper in [1, 5]:  # cotton, chiffon
            score += 2.0
        if fabric_lower in [1, 5]:
            score += 1.0
        if pattern_upper in [0, 3]:  # floral, pure color
            score += 1.5
        if pattern_lower in [0, 3]:
            score += 0.5
        if sleeve_length in [0, 1]:  # sleeveless, short sleeve
            score += 2.0
        if outer == 1:  # No outerwear
            score += 1.0
        if covers_navel == 1:
            score += 0.5

    # Winter: prefer warm fabrics (furry, knitted, leather), dark colors, long sleeves, outerwear like cardigan
    elif season in ["winter", "cold"]:
        if fabric_upper in [2, 3, 4]:  # leather, furry, knitted
            score += 2.5
        if fabric_outer in [2, 3, 4]:
            score += 1.5
        if sleeve_length == 3:  # long sleeve
            score += 2.0
        if outer == 0:  # cardigan
            score += 2.0
        if pattern_upper == 3:  # pure color (often darker)
            score += 1.0

    # Spring: prefer light fabrics, medium sleeves, floral patterns, some layering allowed
    elif season == "spring":
        if fabric_upper in [1, 5]:
            score += 1.5
        if pattern_upper == 0:  # floral
            score += 2.0
        if sleeve_length == 2:  # medium sleeve
            score += 1.5
        if outer in [0, 1]:  # cardigan or no outerwear
            score += 1.0

    # Fall / Autumn: warmer fabrics but lighter than winter, layering with cardigan, warm colors
    elif season in ["fall", "autumn"]:
        if fabric_upper in [1, 2, 4]:  # cotton, leather, knitted
            score += 2.0
        if outer == 0:
            score += 2.0
        if sleeve_length in [2, 3]:  # medium or long sleeves
            score += 1.5
        if pattern_upper in [4, 6]:  # lattice or color block (warm tones)
            score += 1.0

    # Rainy or Dry seasons: prefer water-resistant fabrics (leather), minimal outerwear
    elif season == "rainy":
        if fabric_upper == 2:  # leather
            score += 2.0
        if outer == 1:  # no outerwear (to avoid getting wet)
            score += 1.0

    elif season == "dry":
        if fabric_upper in [1, 5]:
            score += 1.5
        if outer == 1:
            score += 1.0

    return score

def heuristic_occasion_score(outfit: Dict[str, Any], occasion: Optional[str]) -> float:
    """
    Assign heuristic scores to outfits based on occasion type.
    Args:
        outfit: dict of outfit attributes
        occasion: occasion string (e.g., 'wedding', 'party', 'gym', 'work')
    Returns:
        float score based on matching occasion heuristics
    """
    if not occasion:
        return 0.0

    occasion = occasion.lower()
    score = 0.0

    sleeve_length = outfit.get("sleeve_length")
    outer = outfit.get("outer")
    socks = outfit.get("socks")
    hat = outfit.get("hat")
    glasses = outfit.get("glasses")
    neckwear = outfit.get("neckwear")
    waist_acc = outfit.get("waist_acc")
    fabric_upper = outfit.get("fabric_upper")

    # Formal occasions: wedding, party, ceremony, interview, work, business, meeting
    if occasion in [
        "wedding", "party", "ceremony", "interview", "work", "office",
        "business", "meeting", "graduation"
    ]:
        if outer == 0:  # cardigan or similar outerwear is good for formal
            score += 2.0
        if sleeve_length == 3:  # long sleeves preferred
            score += 1.5
        if neckwear == 1:
            score += 1.0
        if waist_acc in [1, 2]:  # belt or clothing accessory
            score += 1.0
        if fabric_upper in [2, 1]:  # leather or cotton fabrics considered formal
            score += 1.0
        if glasses in [1, 2]:  # eyeglasses or sunglasses can add style points
            score += 0.5

    # Casual occasions: casual, holiday, vacation, picnic, date
    elif occasion in ["casual", "holiday", "vacation", "picnic", "date"]:
        if sleeve_length in [0, 1, 2]:  # sleeveless to medium sleeves
            score += 1.5
        if outer == 1:  # no outerwear preferred
            score += 1.0
        if hat == 1:
            score += 0.5
        if socks == 0:
            score += 0.5

    # Sport or gym occasions
    elif occasion in ["sport", "gym"]:
        if socks == 1:
            score += 2.0
        if sleeve_length in [0, 1]:
            score += 1.5
        if fabric_upper in [1, 6]:  # cotton or other flexible fabrics
            score += 1.0
        if waist_acc == 1:
            score += 0.5  # belt might be used in sportswear

    # Office or business casual
    elif occasion in ["office", "business", "work"]:
        if outer in [0, 1]:  # cardigan or no outerwear
            score += 1.5
        if sleeve_length in [2, 3]:  # medium or long sleeves
            score += 1.5
        if waist_acc in [1, 2]:
            score += 1.0
        if neckwear == 1:
            score += 1.0

    # Party or festive
    elif occasion == "party":
        if pattern_upper in [1, 6]:  # graphic or color block
            score += 1.5
        if sleeve_length in [0, 1]:
            score += 1.0
        if waist_acc == 1:
            score += 0.5

    return score
