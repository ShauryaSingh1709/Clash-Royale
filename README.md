# RoyaleForge

Open-source Clash Royale analytics platform . Analyze decks, explore cards, and master the meta with data-driven insights.

## Features

- **Deck Analyzer** - Predict win rates, score deck strength, and classify archetypes
- **Card Explorer** - Browse 97+ cards with filters for rarity, type, and archetype
- **Meta Dashboard** - Visualize meta trends with interactive charts
- **AI Recommendations** - Get card replacement suggestions and find similar decks

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, JavaScript, Chart.js |
| Backend | Python 3.10+, Flask, Gunicorn |
| Containerization | Docker, Docker Compose |
| Machine Learning | Scikit-Learn, Pandas, NumPy |
| Data Processing | CSV-based datasets |

## Requirements

- Python 3.10 or higher
- pip (Python package manager)
- Docker & Docker Compose (for containerized deployment)
- Git

## Installation

### Option 1: Local Setup

```bash
git clone https://github.com/ShauryaSingh1709/Clash-Royale.git
cd Clash-Royale
pip install -r requirements.txt
```

### Option 2: Docker (Recommended)

```bash
git clone https://github.com/ShauryaSingh1709/Clash-Royale.git
cd Clash-Royale
docker-compose up --build
```

## Quick Start

### Local

```bash
python scripts/generate_dataset.py
python -m backend.app
```

### Docker

```bash
docker-compose up --build
```

Navigate to `http://127.0.0.1:5000` in your browser.

## Docker Configuration

The project includes a production-ready Docker setup with multi-layered health checks and persistent volumes.

### Dockerfile Features

- **Base Image**: `python:3.10.13-slim-bookworm` for minimal footprint
- **Non-root User**: Runs as `royaleforge` user for security
- **Gunicorn WSGI**: Production-grade server with 2 workers, 4 threads
- **Health Checks**: Container-level health monitoring via `/api/v1/health`
- **Optimized Build**: Layer caching for faster rebuilds

### Docker Compose Services

| Service | Description |
|---------|-------------|
| `royaleforge` | Main application container |

### Volumes

| Volume | Purpose |
|--------|---------|
| `./dataset` | Persist card/deck/battle data |
| `./logs` | Application log storage |

### Useful Commands

```bash

docker-compose up -d --build
docker-compose logs -f royaleforge
docker-compose down
docker-compose up --build
docker inspect --format='{{.State.Health.Status}}' royaleforge-app
```

## Project Structure

```
Clash-Royale/
├── backend/
│   ├── app.py                      # Flask application entry point
│   ├── config/
│   │   └── settings.py             # Configuration constants
│   ├── models/
│   │   ├── card.py                 # Card data model
│   │   ├── deck.py                 # Deck data model
│   │   └── battle.py               # Battle data model
│   ├── routes/
│   │   ├── card_routes.py           # Card API endpoints
│   │   ├── deck_routes.py           # Deck analysis endpoints
│   │   ├── meta_routes.py           # Meta statistics endpoints
│   │   └── recommendation_routes.py   # Recommendation endpoints
│   ├── services/
│   │   ├── card_analyzer.py          # Card analysis service
│   │   ├── deck_analyzer.py          # Deck analysis service
│   │   └── meta_analyzer.py          # Meta analysis service
│   ├── ml/
│   │   ├── model_loader.py           # ML model loading
│   │   └── predictor.py              # Prediction interface
│   └── utils/
│       ├── dataset_loader.py         # Data loading utilities
│       ├── data_cleaner.py           # Data validation
│       └── logger.py                 # Logging configuration
├── frontend/
│   ├── css/                        # Stylesheets
│   ├── js/                         # JavaScript modules
│   └── *.html                      # Page templates
├── dataset/
│   ├── raw/                        # Original datasets
│   └── processed/                  # Cleaned data
├── notebooks/                      # Jupyter notebooks
└── scripts/
    └── generate_dataset.py           # Dataset generation
```

## API Reference

### Deck Analysis

```bash
POST /api/v1/decks/analyze
Content-Type: application/json

{
  "cards": ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons", "Fireball", "The Log", "Cannon", "Ice Golem"]
}
```

Response:

```json
{
  "success": true,
  "deck": { /* deck composition */ },
  "scoring": {
    "win_rate": { "predicted_win_rate": 55.5, "confidence": "High" },
    "strength": { "strength_score": 78.5, "grade": "B" },
    "archetype": { "predicted_archetype": "Hog Cycle", "confidence": 85.0 }
  },
  "strengths": ["Fast cycle potential", "Good spell coverage"],
  "weaknesses": ["Few troops in deck"]
}
```

### Card Endpoints

- `GET /api/v1/cards` - All cards
- `GET /api/v1/cards/{name}` - Card details
- `GET /api/v1/cards/search?q={query}` - Search cards
- `GET /api/v1/cards/top/win-rate?n=10` - Top win rate cards
- `GET /api/v1/cards/top/usage?n=10` - Top usage cards
- `GET /api/v1/cards/stats` - Card statistics

### Meta Endpoints

- `GET /api/v1/meta/summary` - Meta summary
- `GET /api/v1/meta/trends` - Seasonal trends

### Recommendation Endpoints

- `POST /api/v1/recommend/full` - Full deck analysis
- `POST /api/v1/recommend/similar` - Similar decks
- `POST /api/v1/recommend/replacements` - Card replacements
- `GET /api/v1/recommend/archetype/{name}` - Archetype recommendations

## Machine Learning Models

| Model | Algorithm | Purpose |
|-------|-----------|---------|
| Win Rate Predictor | Random Forest Regressor | Predict deck win rate percentage |
| Deck Strength Scorer | Gradient Boosting | Score deck strength (0-100 scale) |
| Archetype Classifier | Random Forest Classifier | Classify deck archetype |
| Similar Deck Finder | K-Nearest Neighbors | Find similar decks |

## Dataset

- **Cards**: 97+ Clash Royale cards with stats
- **Decks**: 500+ competitive decks
- **Battles**: 5,000 simulated battles
- **Meta Stats**: Seasonal usage and win rate data

## Contributing

Read the [contributing guide](CONTRIBUTING.md) for development setup and contribution guidelines.

## License

MIT License | Open-source and free to use

## Disclaimer

Not affiliated with Supercell. Clash Royale is a registered trademark of Supercell Only.
