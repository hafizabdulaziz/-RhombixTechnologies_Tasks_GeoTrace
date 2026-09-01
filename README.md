# GeoTrace — Intelligent Geolocation Intelligence Platform

GeoTrace is a production-oriented Python application for **IP and domain geolocation intelligence**. It accepts a public IP address or domain, resolves and analyzes the target through a provider-based geolocation service, presents network and geographic information through a responsive web dashboard, visualizes the approximate location on an interactive map, and stores lookup history for later inspection.

The project was initially developed for a **Python programming internship task** and was subsequently expanded into a more structured portfolio project with layered backend architecture, provider failover, validation, persistence, testing, containerization, CI/CD, database migrations, and structured request logging.

> **Important:** IP geolocation provides an approximate network location. It is not GPS tracking and should not be interpreted as the exact physical location of a person, device, or building.

---

## Overview

GeoTrace follows a layered lookup workflow:

```text
IP Address / Domain
        │
        ▼
Input Classification & Validation
        │
        ├── Invalid / Private / Local Target
        │
        ▼
Domain Resolution (when required)
        │
        ▼
Geolocation Provider
        │
        ▼
Provider Failover & Error Handling
        │
        ▼
Normalized Geolocation Result
        │
        ├───────────────┬───────────────┬───────────────┐
        ▼               ▼               ▼               ▼
    Dashboard      Interactive       History         Analytics
     Metrics          Map            Storage          Metrics
        │               │               │
        └───────────────┴───────────────┘
                        │
                        ▼
                 User-Facing Result
```

The application keeps the presentation layer lightweight while moving validation, provider communication, normalization, persistence, and business logic into dedicated backend components.

## Key Features

### IP Geolocation Lookup
GeoTrace accepts public IPv4 and IPv6 addresses and retrieves available geographic and network intelligence from the configured geolocation provider.

### Domain Lookup
GeoTrace can accept domains/hostnames and resolve them before performing geolocation.

### Multi-Provider / Failover Architecture
The provider layer handles provider timeouts, connection failures, and API errors to ensure lookup reliability. This allows the service layer to attempt alternative providers when configured and prevents individual provider failures from unnecessarily breaking the complete lookup workflow.

### Input Validation
Distinguishes between valid public targets and local/private loopback addresses.

### Interactive Mapping
Visualize results on an interactive map using **Leaflet.js**.

### Lookup History
Successful lookups are persisted in SQLite (Development) or PostgreSQL (Production).

### Structured Error Handling
The API uses structured error handling to provide controlled responses when provider services or internal components fail.

### Request / Application Logging
The backend includes structured logging to make request processing and service-level failures easier to diagnose.

## Architecture

GeoTrace follows a layered backend structure:

```text
Frontend
   │
   ▼
FastAPI API Layer
   │
   ▼
Service / Business Logic
   │
   ├── Input Validation
   ├── Domain Resolution
   ├── Provider Selection
   ├── Failover Handling
   └── Result Normalization
   │
   ▼
Provider Layer
   │
   ▼
External Geolocation APIs

API Layer
   │
   ▼
SQLAlchemy ORM
   │
   ├── SQLite (Local Development)
   └── PostgreSQL / Neon (Production)
```

## Technology Stack

| Layer               | Technology        |
| ------------------- | ----------------- |
| Language            | Python            |
| API Framework       | FastAPI           |
| ORM                 | SQLAlchemy        |
| Database            | SQLite / PostgreSQL (Neon) |
| Migrations          | Alembic           |
| Frontend            | HTML5             |
| Styling             | Tailwind CSS      |
| Mapping             | Leaflet.js        |
| Testing             | Pytest            |
| Containerization    | Docker            |
| CI/CD               | GitHub Actions    |

## Project Structure

```text
GeoEngine_Repo/
│
├── api/
│   └── index.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── src/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── providers/
│   └── services/
│
├── tests/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt
├── alembic.ini
├── vercel.json
├── Dockerfile
└── README.md
```

## API

### `POST /api/v1/lookup`
Performs a geolocation lookup for an IP address or domain.

### `GET /api/v1/history`
Returns stored lookup history.

### `DELETE /api/v1/history/delete/{id}`
Deletes a specific historical lookup record.

### `GET /api/v1/health`
Provides a lightweight health/status endpoint.

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
