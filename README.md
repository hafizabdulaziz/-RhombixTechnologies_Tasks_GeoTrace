# GeoTrace — Intelligent Geolocation Intelligence Platform

GeoTrace is a production-oriented Python application for **IP and domain geolocation intelligence**.

It accepts a public IP address or domain, resolves and analyzes the target through a provider-based geolocation service, presents the resulting network and geographic information through a web dashboard, plots the approximate location on an interactive map, and stores lookup history for later inspection.

The project was initially developed to satisfy a Python geolocation internship task and was subsequently expanded into a more structured portfolio project with a layered backend architecture, provider failover, validation, persistence, testing, containerization, CI, and structured request logging.

> **Important:** IP geolocation provides an approximate network location. It is not GPS tracking and should not be interpreted as the exact physical location of a person, device, or building.

---

## Overview

The primary workflow is:

```text
IP Address / Domain
        ↓
Input Classification & Validation
        ↓
Domain Resolution (when required)
        ↓
Geolocation Provider
        ↓
Provider Failover / Error Handling
        ↓
Normalized Geolocation Result
        ↓
┌───────────────┬────────────────┬────────────────┐
│               │                │                │
▼               ▼                ▼                ▼
Dashboard      Interactive      History         Analytics
Metrics        Map             Storage          Metrics
        \          |              /
         \         |             /
          └────────┴─────────────┘
```

The application is designed to keep the user-facing layer simple while moving business logic into dedicated backend services.

---

## Key Features

### IP Geolocation Lookup
Analyze public IPv4 and IPv6 addresses and retrieve available geographic and network information.

### Domain Lookup
GeoTrace can accept domains/hostnames and resolve them before performing geolocation.

### Multi-Provider Failover
The provider layer handles provider timeouts, connection failures, and API errors to ensure lookup reliability.

### Input Validation
Distinguishes between valid public targets and local/private loopback addresses.

### Interactive Mapping
Visualize results on an interactive map using **Leaflet.js**.

### Lookup History
Successful lookups are persisted in SQLite (Development) or PostgreSQL (Production).

---

## Technology Stack

| Layer            | Technology                     |
| ---------------- | ------------------------------ |
| Language         | Python                         |
| API Framework    | FastAPI                        |
| ORM              | SQLAlchemy                     |
| Database         | SQLite / PostgreSQL (Neon)     |
| Frontend         | HTML5, Tailwind CSS, Leaflet.js |
| Testing          | Pytest                         |
| CI/CD            | GitHub Actions                 |

---

## Local Development

1. **Clone the repository:**
   `git clone https://github.com/hafizabdulaziz/-RhombixTechnologies_Tasks_GeoTrace.git`
2. **Create virtual environment:** `python -m venv .venv`
3. **Activate:** `.\.venv\Scripts\activate` (Windows)
4. **Install dependencies:** `pip install -r requirements.txt`
5. **Start server:** `python -m uvicorn src.api.main:app --reload`

---

## Production Deployment

GeoTrace is configured for deployment on Vercel with Neon PostgreSQL.

1. **Database:** Ensure `DATABASE_URL` is configured in Vercel Environment Variables.
2. **Migrations:** Managed via Alembic; handled automatically by CI/CD pipeline on `main` branch.
3. **CI/CD:** GitHub Actions ensures tests pass before migrations are applied.

---

## License
Add an explicit open-source license here only if one has actually been selected for this repository.
