# Rule-Based Decision Tree — Expanded Story

This decision tree describes how the AI-Driven Outfit Recommender makes its choices using a clear, step-by-step, rule-based (if-then) logic.

---

## Top-Level Decision Flow

### 1. **Gender Filtering (First Branch)**
- **IF** the outfit's gender matches the user's gender **OR** the outfit is unisex  
  → **then** include outfit, **else** exclude.

### 2. **Body Shape Filtering**  
- **IF** the user's body shape is in the supported list (Hourglass, Triangle, Inverted Triangle, Rectangle, Oval)  
  → **then** continue, **else** stop and return "unsupported body shape".

### 3. **Prompt Feature Extraction (AI Branch)**
- **IF** the user prompt contains keywords for style, season, occasion, or features  
  → **then** extract them, **else** set defaults (e.g., style = 'Casual').

### 4. **Feature Matching**
- **IF** extracted features are present
  - For each required feature (e.g., "short sleeve", "cotton"):
    - **IF** the outfit's attribute matches the feature  
      → **then** continue, **else** exclude outfit.

### 5. **Scoring Branch**
- **IF** outfit passes all above filters  
  → **then** calculate:
    - Style Score (rule-based, using style matrix)
    - Body Shape Score (rule-based, using body shape matrix)
    - Sum for Total Score

### 6. **Ranking and Return**
- **IF** more than one outfit remains  
  → **then** rank by Total Score, return top N.
- **ELSE**  
  → return a message: "No suitable outfits found."

---

## Example Path Through the Tree

**User Input:**  
- Gender: male
- Body Shape: Triangle
- Prompt: "Looking for a formal outfit for winter, long sleeves and wool preferred"

**Branching:**

1. **Gender Match?**  
   - IF outfit is male or unisex → keep

2. **Body Shape Supported?**  
   - IF Triangle → continue

3. **Prompt Extraction:**  
   - Style: formal  
   - Season: winter  
   - Features: long sleeves, wool

4. **Feature Match?**  
   - IF outfit has long sleeves AND wool → keep  
   - ELSE → discard

5. **Scoring:**  
   - Calculate Style Score (formal)  
   - Calculate Body Shape Score (Triangle)  
   - Add for Total Score

6. **Ranking:**  
   - Sort by Total Score  
   - Return top 3 outfits

---

## Visual Decision Tree

```mermaid
flowchart TD
    Start([Start]) --> GenderCheck{Gender Match?}
    GenderCheck -- Yes --> BodyShapeCheck{Body Shape Supported?}
    GenderCheck -- No --> Exclude1([Exclude Outfit])

    BodyShapeCheck -- Yes --> ParsePrompt[Parse Prompt for Features]
    BodyShapeCheck -- No --> Exclude2([Return: Unsupported Body Shape])

    ParsePrompt --> FeatureCheck{All Features Match?}
    FeatureCheck -- Yes --> ScoreBranch[Score Outfit]
    FeatureCheck -- No --> Exclude3([Exclude Outfit])

    ScoreBranch --> Ranking[Rank by Score]
    Ranking --> ReturnTopN([Return Top N Outfits])
```

---

## Notes

- Each branch is a clear IF-THEN statement.
- Filtering is strict: failing any branch means exclusion.
- Scoring only happens after all filters pass.
- Ranking is based solely on computed scores.