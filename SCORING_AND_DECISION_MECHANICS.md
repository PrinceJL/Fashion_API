# Scoring and Decision Mechanics in the Outfit Recommender

This document explains **how the scoring system works** and how it informs style-based decisions in the AI-Driven Outfit Recommender.

---

## 1. Overview

The recommender uses a **rule-based scoring system** to evaluate how well each outfit matches the user's:
- **Desired style** (e.g., Casual, Formal)
- **Body shape** (e.g., Hourglass, Triangle, etc.)
- **Specified features** (extracted from prompt: "short sleeve", "cotton", etc.)

Outfits are filtered by gender and then scored. The highest combined scores are recommended.

---

## 2. Scoring Matrices

There are **two scoring matrices** loaded from Google Sheets:

- **Style Score Matrix:**  
  Scores for how well each attribute (like sleeve length, fabric) fits a specific style.
  - Example: "Short Sleeve" might score 10 for Casual, but only 5 for Formal.

- **Body Shape Score Matrix:**  
  Scores for how well each attribute flatters a specific body shape.
  - Example: "Belt" accessory may score 9 for Hourglass but 5 for Rectangle.

Each matrix is structured as:

| Attribute       | Value         | Style/Body Shape 1 | Style/Body Shape 2 | ... |
|-----------------|--------------|--------------------|--------------------|-----|
| sleeve_length   | Short Sleeve  | 10                 | 5                  | ... |
| fabric_upper    | cotton        | 8                  | 6                  | ... |

---

## 3. The Scoring Algorithm

For each outfit that passes earlier filters:

1. **Style Score Calculation**  
   For each relevant attribute (e.g., `sleeve_length`, `waist_acc`, `fabric_upper`):
   - Get the attribute's value in the outfit (e.g., "Short Sleeve").
   - Look up the score for the user's desired style in the style matrix.
   - Sum scores across all attributes for the **total style score**.

2. **Body Shape Score Calculation**  
   For each relevant attribute:
   - Get the score for the user's selected body shape in the body shape matrix.
   - Sum for the **total body shape score**.

3. **Combined Score**  
   `Final Score = Style Score + Body Shape Score`

4. **(Optional) Attribute Weights**  
   Each attribute may have a weight (default 1.0). Multiply each attribute's score by its weight before summing, to emphasize or de-emphasize certain features.

---

## 4. How Scoring Informs Decision

### Step-by-Step Example

**User:**  
- Gender: female  
- Body shape: Rectangle  
- Prompt: "I want a formal outfit for work, sleeveless preferred, denim or cotton fabric"

**Process:**  
1. **Gender Filter:** Only "female" or "unisex" outfits remain.
2. **Body Shape Support:** Only "Rectangle" supported.
3. **Prompt Parsing:**  
   - Style: Formal  
   - Features: sleeveless, denim or cotton
4. **Feature Matching:** Outfits must be sleeveless AND either denim or cotton.
5. **Scoring:**  
   - For each matching outfit:
     - Sum style scores (for "Formal") across attributes.
     - Sum body shape scores (for "Rectangle") across same attributes.
     - Add together.

6. **Ranking:**  
   Outfits are sorted by total score. Top N are recommended.

---

## 5. Why This Works

- **Personalization:** Each attribute's effect on a style/body shape is encoded by human experts or data, so recommendations are tailored.
- **Transparency:** The score breakdown can be shown to the user (e.g., "this outfit is formal because...").
- **Flexibility:** You can add more styles, shapes, or features by updating the score matrices.

---

## 6. Decision Flow Recap

1. **If** gender matches → keep  
2. **If** body shape is supported → keep  
3. **If** features (from prompt) match outfit → keep  
4. **Score** for style and body shape  
5. **Add scores** for final ranking  
6. **Recommend** highest scorers

---

## 7. Example Table

| Attribute      | Value         | Style: Formal | Body: Rectangle |
|----------------|--------------|---------------|-----------------|
| sleeve_length  | Sleeveless   | 3             | 5               |
| fabric_upper   | denim        | 3             | 7               |
| waist_acc      | No           | 3             | 6               |
| **Sum**        |              | **9**         | **18**          |
| **Total**      |              |               | **27**          |

---

