# GeoTrace — IP Geolocation & Network Intelligence Platform

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

Analyze public IPv4 and IPv6 addresses and retrieve available geographic and network information such as:

* IP address
* country
* region
* city
* latitude
* longitude
* provider
* lookup latency

The result is presented directly in the dashboard.

### Domain Lookup

GeoTrace can accept domains/hostnames and resolve them before performing geolocation.

Example:

```text
github.com
        ↓
DNS / hostname resolution
        ↓
Resolved public IP
        ↓
Geolocation lookup
```

This makes the application useful when the user knows a hostname rather than the underlying IP address.

### Multi-Provider Failover

The provider layer is designed so that a provider failure does not automatically terminate the whole lookup flow.

Depending on the configured providers, the service can handle conditions such as:

* provider timeout
* connection failure
* HTTP/API failure
* malformed provider response
* unavailable provider
* total provider failure

The system attempts the configured provider sequence and returns a controlled failure when no provider can produce a usable result.

### Input Validation

GeoTrace distinguishes between different target types and rejects unsupported inputs before unnecessary provider calls are made.

Examples include:

```text
8.8.8.8               → public IPv4
1.1.1.1               → public IPv4
2606:4700:4700::1111  → public IPv6
example.com            → domain
127.0.0.1              → local loopback
192.168.1.1            → private address
999.999.999.999       → invalid IPv4
```

Local/private/loopback targets are handled as non-public addresses rather than being presented as meaningful public geolocation results.

### Interactive Mapping

Lookup results can be visualized using **Leaflet.js**.

The dashboard map can:

* display the current lookup location
* show geographic coordinates
* provide a marker and popup
* plot stored historical lookup locations

Map tiles are provided through OpenStreetMap-compatible Leaflet tile infrastructure.

### Lookup History

Successful lookup information is persisted in SQLite through SQLAlchemy.

The History section allows the user to:

* review previous lookups
* inspect stored location information
* plot historical records on the map
* delete individual history records

History data survives page refreshes because it is stored in the database rather than only in browser memory.

### History Record Deletion

Each historical record supports a dedicated delete action.

The deletion flow:

```text
User selects Delete
        ↓
Confirmation
        ↓
DELETE API request
        ↓
Database record removed
        ↓
History refreshed
        ↓
Deleted row disappears
```

Only the selected record is removed; remaining records stay intact.

### Lookup Analytics

GeoTrace derives useful summary information from historical lookup data.

This provides a lightweight view into the application's lookup activity without turning the dashboard into an unnecessary analytics-heavy interface.

### Structured Request Logging

The API layer includes request-oriented logging with request IDs.

This makes it easier to correlate:

```text
Request
  ↓
API
  ↓
Service
  ↓
Provider
  ↓
Response / Failure
```

during debugging and operational inspection.

Sensitive credentials and secrets are not intended to be written to logs.

---

# Architecture

GeoTrace follows a layered architecture intended to separate responsibilities.

## Core Layer

The core layer contains shared domain concepts, validation utilities, interfaces, and structures that should not depend heavily on the presentation layer.

This helps keep the business rules independent from the browser and CLI.

## Provider Layer

Providers implement the external geolocation integrations behind a common provider contract.

Conceptually:

```text
GeolocationProvider
        │
        ├── Provider A
        ├── Provider B
        └── Future Providers
```

This makes provider replacement or extension easier without moving provider-specific logic into the API routes.

## Factory / Provider Selection

Provider creation and selection is centralized rather than duplicated throughout the application.

This keeps the service layer focused on orchestration rather than construction details.

## Service Layer

The service layer coordinates operations such as:

* input validation
* provider execution
* failover
* result normalization
* persistence
* history operations
* map-related data preparation

The API layer should therefore remain relatively thin.

## Repository / Persistence Layer

Database interaction is kept behind dedicated persistence/repository components.

The goal is to isolate SQLAlchemy/SQLite details from higher-level application logic.

## API Layer

FastAPI exposes the HTTP interface used by the dashboard.

Current API responsibilities include:

```text
GET  /
POST /api/v1/lookup
GET  /api/v1/history
DELETE /api/v1/history/delete/{id}
GET  /api/v1/health
```

The exact implementation is maintained in the `src/api` layer.

## Web Layer

The frontend is implemented as a server-rendered dashboard with HTML, Tailwind CSS, JavaScript, and Leaflet.js.

The frontend communicates with the FastAPI API rather than implementing the geolocation business logic itself.

---

# Technology Stack

| Layer            | Technology                     |
| ---------------- | ------------------------------ |
| Language         | Python                         |
| API Framework    | FastAPI                        |
| ASGI Server      | Uvicorn                        |
| ORM              | SQLAlchemy                     |
| Database         | SQLite                         |
| Frontend         | HTML5, JavaScript              |
| UI Styling       | Tailwind CSS                   |
| Mapping          | Leaflet.js                     |
| Map Tiles        | OpenStreetMap-compatible tiles |
| Testing          | Pytest                         |
| Containerization | Docker / Docker Compose        |
| CI               | GitHub Actions                 |

---

# Project Structure

```text
GeoEngine_Repo/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── config/
│
├── docs/
│   ├── PLAN.md
│   └── baseline-audit.md
│
├── src/
│   ├── api/
│   │   └── main.py
│   │
│   ├── core/
│   │
│   ├── providers/
│   │
│   ├── database/
│   │
│   ├── services/
│   │
│   ├── cli/
│   │
│   └── web/
│       └── templates/
│           └── index.html
│
├── tests/
│   ├── test_api.py
│   ├── test_api_error_handling.py
│   ├── test_failover_scenarios.py
│   ├── test_history_delete.py
│   └── test_system.py
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# API

## `POST /api/v1/lookup`

Performs a geolocation lookup for an IP address or domain.

Typical flow:

```text
Input
  ↓
Classification
  ↓
Validation
  ↓
Resolution (domain when required)
  ↓
Provider lookup
  ↓
Normalized result
  ↓
Persistence
```

A successful response contains the information required by the dashboard and map layer.

---

## `GET /api/v1/history`

Returns stored lookup history.

The response is consumed by the dashboard to populate the Recent Lookups section.

---

## `DELETE /api/v1/history/delete/{id}`

Deletes a specific historical lookup record.

The endpoint is intentionally scoped to one record rather than providing an unrestricted history wipe operation.

---

## `GET /api/v1/health`

Provides a lightweight health/status endpoint for application and service inspection.

---

# Example Usage

### Public IP

```text
8.8.8.8
```

The application can return available network and geographic information and plot the approximate location on the map.

### Another public IP

```text
1.1.1.1
```

### Domain

```text
github.com
```

The application can resolve the hostname before performing the lookup.

### Local address

```text
127.0.0.1
```

This is a local loopback address and is not treated as a meaningful public geolocation target.

### Invalid address

```text
999.999.999.999
```

The application should reject it without crashing.

---

# Error Handling

GeoTrace is designed around controlled failures rather than exposing raw backend exceptions to users.

Examples include:

```text
Invalid Input
        ↓
Validation Error

Provider Timeout
        ↓
Failover / Provider Error Handling

All Providers Fail
        ↓
Controlled Lookup Failure

Database Error
        ↓
Controlled Persistence Error

Frontend Runtime Error
        ↓
Visible UI Error State
```

The goal is to make failure behavior understandable without leaking internal implementation details.

---

# Testing

The repository includes API, system, error-handling, failover, and history-deletion coverage.

Run the complete test suite with:

```bash
pytest -v
```

The latest verified local test suite contains **12 passing tests**.

The test suite includes coverage for areas such as:

* dashboard serving
* API health
* API history
* lookup validation
* malformed input
* successful lookup
* geolocation data handling
* provider interface behavior
* API error handling
* provider failover scenarios
* History record deletion

External provider behavior is tested through controlled test paths/mocks where appropriate so normal automated tests do not depend on unpredictable third-party API responses.

---

# Docker

GeoTrace includes Docker configuration for a reproducible application environment.

## Build and Run

```bash
docker-compose up --build
```

Then open:

```text
http://localhost:8000
```

The Docker setup is intended to make local reproduction easier and reduce environment-specific setup differences.

---

# Local Development

## 1. Clone the repository

```bash
git clone https://github.com/hafizabdulaziz/-RhombixTechnologies_Tasks_GeoEngine.git
cd -RhombixTechnologies_Tasks_GeoEngine
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the environment

### Windows

```powershell
.\.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure environment variables

Copy the example environment file:

```text
.env.example
```

to:

```text
.env
```

Then populate the required configuration values.

Do not commit `.env`.

## 6. Start the development server

```bash
python -m uvicorn src.api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

# Configuration

Environment-specific values should be kept outside the source code where practical.

Use:

```text
.env.example
```

as the reference for required configuration.

Never commit:

```text
.env
```

or real API credentials.

---

# CI

GeoTrace uses GitHub Actions for automated verification.

The CI workflow installs project dependencies and runs the test suite on repository changes.

The purpose of CI is to detect regressions before code changes are treated as part of the stable main branch.

---

# Security Notes

GeoTrace is designed with basic defensive engineering practices including:

* environment-based secret configuration
* `.env` exclusion from Git
* database files excluded from the repository
* input validation
* controlled API errors
* provider failure handling
* structured request logging
* avoidance of credential exposure in logs

IP geolocation is informational and approximate. It should not be treated as a substitute for GPS, device tracking, identity verification, or exact physical-location services.

---

# Design Decisions

## Why FastAPI?

FastAPI provides:

* typed request/response models
* validation
* automatic API documentation
* ASGI-based request handling
* a natural fit for a Python API service

## Why SQLAlchemy?

SQLAlchemy provides a structured persistence layer and separates application logic from raw SQL/database handling.

## Why SQLite?

SQLite keeps the project simple to run locally while still providing real persistent storage for lookup history.

It is appropriate for the current portfolio/local deployment scope, while a larger deployment could move the persistence layer to another relational database.

## Why Provider Abstraction?

External geolocation APIs can fail, change, or become unavailable.

Keeping provider implementations behind a common interface makes the system easier to extend and makes failover possible.

## Why Leaflet?

Leaflet provides a lightweight way to present geospatial results interactively without requiring a large frontend framework.

---

# Limitations

GeoTrace has intentionally defined boundaries.

### IP Geolocation Accuracy

IP-based geographic information is approximate and depends on the underlying provider/database.

### External Provider Availability

Provider APIs can experience:

* outages
* rate limits
* latency
* inaccurate data
* response changes

GeoTrace includes failover/error handling, but no application can guarantee external provider availability.

### SQLite Scale

SQLite is convenient for this project but is not necessarily the ideal database for a large multi-user production deployment.

### Local Deployment

The current project is designed primarily as a portfolio and development application with production-oriented engineering practices.

It is not presented as a globally deployed SaaS platform.

---

# Internship Context

GeoTrace was originally developed to satisfy the **Python Development — Geolocation Tracker** requirement of the Rhombix Technologies internship.

The original task was:

> Develop a script that fetches the user's geolocation using an IP address and displays it on a map.

The project extends that basic requirement with:

* web dashboard
* API layer
* validation
* provider failover
* persistent history
* history management
* analytics
* interactive mapping
* structured logging
* automated tests
* Docker
* CI

The internship requirement remains the foundation of the project; the additional engineering work exists to demonstrate practical Python/backend development skills.

---

# Future Improvements

Potential future work, outside the current frozen release, could include:

* authentication and access control
* PostgreSQL-backed deployment
* background jobs
* richer rate limiting
* provider performance dashboards
* API key management
* large-scale bulk processing
* cloud deployment
* centralized observability
* automated database migrations and backup strategies

These are intentionally kept as future improvements rather than being represented as existing functionality.

---

# Portfolio Highlights

GeoTrace demonstrates practical experience with:

```text
Python
FastAPI
REST APIs
Input Validation
Service Layer Architecture
Strategy Pattern
Factory Pattern
Repository Pattern
Provider Failover
Error Handling
SQLAlchemy
SQLite
Leaflet.js
Async / Concurrent Processing
Structured Logging
Request IDs
Pytest
Docker
GitHub Actions
Git
```

More importantly, the project demonstrates the engineering cycle:

```text
Requirement
   ↓
Implementation
   ↓
Testing
   ↓
Failure Detection
   ↓
Debugging
   ↓
Regression Testing
   ↓
Documentation
   ↓
CI Verification
   ↓
Release
```

---

# Repository

GitHub:

```text
https://github.com/hafizabdulaziz/-RhombixTechnologies_Tasks_GeoEngine
```

---

## License

Add an explicit open-source license here only if one has actually been selected for this repository.

---

## Project Status

**Release Candidate / Frozen Portfolio Build**

The current repository represents a stable portfolio-focused release. Future feature work should be treated as a new development cycle rather than mixed into the frozen release without regression testing.
