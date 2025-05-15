import re
from src.occasion_mapping import OCCASION_TO_STYLES

# Define a synonym mapping for styles
STYLE_SYNONYMS = {
    "comfortable": "Casual",
    "chic": "Elegant",
    "laid-back": "Casual",
    "trendy": "Streetwear",
    "not too formal": "Casual",
    "simple": "Minimalist",
    "fancy": "Elegant",
}

def parse_prompt(prompt: str):
    """
    Parse the user's prompt to extract the desired occasion, style, and clothing preferences.

    Args:
    - prompt (str): User's natural language input.

    Returns:
    - dict: Extracted details including occasion, styles, and clothing preferences.
    """
    # Define common styles and clothing types
    styles = ["Casual", "Formal", "Trendy", "Bohemian", "Minimalist", "Streetwear", "Elegant"]
    clothing_types = ["Jacket", "Dress", "Skirt", "Pants", "Shirt", "Denim", "Suit", "Sweater"]

    # Extract styles mentioned in the prompt
    extracted_styles = []
    for synonym, style in STYLE_SYNONYMS.items():
        if synonym in prompt.lower():
            extracted_styles.append(style)

    # Extract clothing types mentioned in the prompt
    extracted_clothing = [clothing for clothing in clothing_types if re.search(rf"\b{clothing}\b", prompt, re.IGNORECASE)]

    # Extract occasion keywords from the prompt
    extracted_occasions = [occasion for occasion in OCCASION_TO_STYLES if re.search(rf"\b{occasion}\b", prompt, re.IGNORECASE)]

    # Map occasions to styles
    occasion_styles = []
    for occasion in extracted_occasions:
        occasion_styles.extend(OCCASION_TO_STYLES[occasion])

    # Combine detected styles with occasion styles
    all_styles = list(set(extracted_styles + occasion_styles))  # Remove duplicates

    # Fallback to "casual" if no style is explicitly mentioned
    if not all_styles:
        all_styles = ["casual"]

    return {
        "styles": all_styles,
        "clothing_types": extracted_clothing,
        "occasions": extracted_occasions
    }