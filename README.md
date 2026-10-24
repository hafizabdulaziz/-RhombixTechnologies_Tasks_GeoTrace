# GeoTrace — Geolocation Intelligence Platform

An IP and domain geolocation intelligence platform built with Python, FastAPI, and SQLAlchemy.

## Overview

GeoTrace resolves, analyzes, and visualizes network and geographic intelligence for public IP addresses and domain hostnames. The platform validates targets, queries upstream geolocation providers with automatic failover, renders results on an interactive map, and persists lookup history for subsequent inspection.

Initially engineered for a Python programming internship task, the project was structured with a layered backend architecture incorporating provider resilience, data validation, database migrations, containerization, CI/CD automation, and structured logging.

> **Note on Geolocation Accuracy**: IP geolocation establishes approximate network-routing locations based on ISP allocations. It does not provide real-time GPS coordinates and should not be treated as a physical device or person tracker.

## Lookup Workflow

```text
IP Address / Domain
        │
        ▼
Input Classification & Validation
        │
        ├── Invalid / Private / Local Loopback Target
        │
        ▼
Domain Resolution (DNS)
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
                 User Presentation
```

## Key Features

- **IP Geolocation**: Accepts public IPv4 and IPv6 addresses to query geographical coordinates, ASN details, and ISP network metadata.
- **Domain Resolution**: Resolves hostnames to IP addresses prior to provider lookup.
- **Provider Failover Architecture**: Resilient client layer that handles provider timeouts and API failures by failing over to secondary providers when configured.
- **Target Validation**: Distinguishes valid routable public IP targets from local, private, and loopback CIDR blocks.
- **Interactive Mapping**: Visualizes resolved geographic coordinates dynamically using Leaflet.js.
- **Historical Persistence**: Stores query audit trails in SQLite (local development) or PostgreSQL (hosted environments).
- **Structured Error Handling**: Returns standardized API error responses during external provider downtime or network anomalies.
- **Request Observability**: Incorporates structured application logging to trace request execution and external client interactions.

## Architecture & Project Structure

### Layered Architecture

```text
Frontend (HTML5 / Tailwind CSS / Leaflet.js)
   │
   ▼
FastAPI API Routing Layer
   │
   ▼
Service & Business Logic Layer
   ├── Input Validation & Target Filtering
   ├── Domain Resolution
   ├── Provider Strategy & Failover Logic
   └── Response Normalization
   │
   ▼
Provider Integration Layer
   │
   ▼
External Geolocation APIs
```

### Directory Structure

```text
GeoEngine_Repo/
├── api/
│   └── index.py            # Entry point for serverless hosting
├── alembic/
│   ├── versions/           # Database migration revisions
│   └── env.py              # Migration configuration
├── src/
│   ├── api/                # FastAPI routes and request handling
│   ├── core/               # Configuration settings and logging
│   ├── database/           # SQLAlchemy engine, session, and ORM models
│   ├── providers/          # External geolocation API client wrappers
│   └── services/           # Domain business logic and failover routines
├── tests/                  # Automated Pytest suite
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI workflow
├── requirements.txt        # Python dependency manifest
├── alembic.ini             # Alembic configuration
├── vercel.json             # Vercel deployment specification
└── Dockerfile              # Container definition
```

## Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python | Core application language |
| **Framework** | FastAPI | High-performance asynchronous API framework |
| **Database & ORM** | SQLAlchemy | Relational persistence with SQLite and PostgreSQL (Neon) |
| **Migrations** | Alembic | Database schema versioning and migration engine |
| **Frontend** | HTML5, Tailwind CSS | Responsive dashboard presentation |
| **Mapping** | Leaflet.js | Interactive geographic map visualization |
| **Testing** | Pytest | Automated unit and integration testing |
| **Containerization** | Docker | Container packaging specification |
| **CI / CD** | GitHub Actions | Automated build, test, and linting pipeline |

## API Reference

### `POST /api/v1/lookup`
Performs geolocation analysis for a provided IP address or domain name.

### `GET /api/v1/history`
Retrieves a paginated list of previous lookup records.

### `DELETE /api/v1/history/delete/{id}`
Removes an individual lookup record by identifier.

### `GET /api/v1/health`
Returns system uptime and health verification status.

## Setup & Local Execution

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hafizabdulaziz/-RhombixTechnologies_Tasks_GeoTrace.git
   cd -RhombixTechnologies_Tasks_GeoTrace
   ```

2. **Configure Virtual Environment**:
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Linux / macOS
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Application**:
   ```bash
   python -m uvicorn src.api.main:app --reload
   ```

## Deployment Configuration

GeoTrace supports serverless deployment on Vercel paired with Neon PostgreSQL:
- **Environment**: Ensure `DATABASE_URL` is set in the deployment environment settings.
- **Database Migrations**: Managed via Alembic, applied automatically in CI/CD pipelines following test suite validation.
