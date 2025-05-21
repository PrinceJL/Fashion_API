# Outfit Recommender API — Architecture

```mermaid
flowchart TD
    Client[User/UI] -->|POST /recommend| API[FastAPI Server]
    API -->|parse prompt| NLP[NLP Prompt Parser]
    API -->|load data| Loader[Data Loader]
    API -->|score| Recommender[Recommendation Engine]
    Loader -->|Google Sheets CSV| Dataset[Outfits & Scoring Matrices]
    NLP -->|style, season, features| Recommender
    Recommender -->|top outfits| API
    API --> Client
```
**Modules:**
- **main.py**: API endpoints, request/response handling
- **nlp_prompt_parser.py**: Extracts style/season/features from free text
- **data_loader.py**: Loads outfits, scoring rules from Google Sheets (CSV)
- **recommender.py, scoring.py**: Rule-based recommendation engine