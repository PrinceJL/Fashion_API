# AI-Driven Outfit Recommender API

A RESTful API for outfit recommendations based on user profile and natural language preferences.

## Features

- Accepts gender, body shape, and a free-form prompt (style, season, occasion, features)
- Recommends best-matching outfits using rule-based and AI/NLP scoring
- Loads scoring rules and outfits from live Google Sheets (editable)
- FastAPI-powered (auto-generates OpenAPI docs and Swagger UI)

## API Usage

### Endpoint

```
POST /recommend
```

### Request JSON

```json
{
  "gender": "male",
  "body_shape": "Hourglass",
  "prompt": "I want a formal outfit for a summer wedding, prefer short sleeves and cotton",
  "topk": 3
}
```

### Response JSON

```json
{
  "recommendations": [
    {
      "gender": "male",
      "image_label": "MEN-Pants-id_xxx.jpg",
      "image_url": "https://...",
      "attributes": {
        "sleeve_length": "Short Sleeve",
        "lower_length": "Long",
        ...
      },
      "total_score": 25,
      "style_score": 15,
      "bodyshape_score": 10
    },
    ...
  ]
}
```

### Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Browse docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Project Structure

- `main.py`: FastAPI app and endpoints
- `outfit_recommender/`: Core modules (attributes, loading, NLP, scoring, recommendation)
- `ARCHITECTURE.md`: System diagram
- `RULE_DECISION_TREE.md`: Rule-based logic documentation

## Extendability

- Plug in new scoring rules (Google Sheets)
- Add more attributes or NLP logic
- Deploy as a service or behind authentication