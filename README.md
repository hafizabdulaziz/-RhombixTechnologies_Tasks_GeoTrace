# GeoTrace — Intelligent Geolocation Intelligence Platform

A production-oriented geolocation platform for IP and domain intelligence, provider failover, historical lookup analysis, interactive mapping, and reliable API-driven workflows.

## Features
- **Intelligent Lookup:** Geolocation intelligence for IPs and domains with multi-provider failover.
- **Compact Dashboard:** Production-oriented, responsive UI designed for actionable insights.
- **Robustness:** Resilient service layer with structured error handling (502 Gateway monitoring).
- **Historical Insights:** Integrated history tracking and lookup analytics.
- **Visual Intelligence:** Interactive Leaflet-based live mapping.

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** HTML5, Tailwind CSS, Leaflet.js
- **Infrastructure:** Docker, CI/CD Pipeline

## Getting Started
### Using Docker (Recommended)
```bash
docker-compose up --build
```
Access the dashboard at `http://localhost:8000`

### Local Development
1. Set up a virtual environment: `python -m venv .venv`
2. Activate: `source .venv/bin/activate` (or `.\.venv\Scripts\activate` on Windows)
3. Install: `pip install -r requirements.txt`
4. Execute: `python -m uvicorn src.api.main:app --reload`
