# GeoTrace Pro

Enterprise-grade IP & Network Intelligence Platform.

## Features
- **Accurate Geolocation:** Lookup IP addresses and domains using reliable providers with failover support.
- **Interactive Mapping:** Real-time geospatial visualization using Leaflet.js.
- **Robust Analytics:** Track lookup history with success metrics.
- **Production Ready:** Dockerized, CI/CD pipeline enabled, structured logging, and robust error handling.

## Getting Started
### Using Docker (Recommended)
```bash
docker-compose up --build
```
Open `http://localhost:8000`

### Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `python -m uvicorn src.api.main:app --reload`

