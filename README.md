# GeoTrace

GeoTrace is an IP geolocation tracking tool built with FastAPI and Leaflet.js, featuring provider failover, history tracking, and structured logging.

## Features
- **Accurate Geolocation:** Lookup IP addresses and domains using reliable providers with failover support.
- **Interactive Mapping:** Geospatial visualization using Leaflet.js.
- **Robust Analytics:** Track lookup history with success metrics.
- **Production Ready:** Dockerized, CI/CD pipeline enabled, structured logging, and robust error handling.

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** HTML5, Tailwind CSS, Leaflet.js
- **Infrastructure:** Docker, GitHub Actions (CI)

## Getting Started
### Using Docker (Recommended)
```bash
docker-compose up --build
```
Open `http://localhost:8000`

### Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `python -m uvicorn src.api.main:app --reload`
