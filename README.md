# LeadForgeAI

LeadForgeAI is a local-first Lead Intelligence Platform designed to help users discover, enrich, analyze, and organize business leads through a desktop-oriented experience.

This repository is currently bootstrapped through `TASK-002`, which establishes the foundational backend, frontend, and database infrastructure without business features, AI workflows, or application modules.

## Current Scope

- FastAPI backend bootstrap
- React + TypeScript + Vite frontend bootstrap
- PostgreSQL database bootstrap
- SQLAlchemy 2.x async session management
- Alembic migration setup
- Health check integration between frontend, backend, and database
- Docker Compose development setup
- Environment variable templates

## Requirements

- Python 3.13
- Node.js 22 or newer
- npm 11 or newer
- Docker Desktop with Docker Compose support

## Installation

1. Copy `.env.example` to `.env`.
2. Optionally copy `backend/.env.example` to `backend/.env` for backend-only local runs.
3. Install backend dependencies:

```bash
cd backend
python -m venv .venv
.venv\Scriptsctivate
pip install -r requirements.txt
```

4. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Development

### Start PostgreSQL with Docker

```bash
docker compose up -d postgres
```

### Run database migrations

```bash
cd backend
alembic upgrade head
```

### Run the backend

```bash
cd backend
.venv\Scriptsctivate
uvicorn main:app --reload
```

The backend starts at [http://localhost:8000](http://localhost:8000).

### Run the frontend

```bash
cd frontend
npm run dev
```

The frontend starts at [http://localhost:5173](http://localhost:5173).

## Docker

Start the full local stack with Docker Compose:

```bash
docker compose up --build
```

Included services:

- PostgreSQL
- FastAPI backend
- React frontend

## Database

The backend uses:

- PostgreSQL
- SQLAlchemy 2.x async engine
- `asyncpg`
- Alembic for schema versioning

This task intentionally creates no business tables. The only database table created at this stage is Alembic's version table.

## Available Endpoints

- `GET /health`
- `GET /api/v1/health`

Healthy response example:

```json
{
  "success": true,
  "status": "healthy",
  "application": "LeadForgeAI",
  "database": "connected"
}
```

If the database is unavailable, the backend returns HTTP `503` with a payload indicating `database: "disconnected"`.

## Folder Structure

```text
LeadForgeAI/
|-- backend/
|   |-- alembic/
|   |   `-- versions/
|   |-- app/
|   |   |-- api/
|   |   |-- core/
|   |   |-- dependencies/
|   |   |-- models/
|   |   |-- repositories/
|   |   |-- schemas/
|   |   |-- services/
|   |   |-- utils/
|   |   `-- main.py
|   |-- alembic.ini
|   |-- Dockerfile
|   |-- main.py
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   |-- Dockerfile
|   |-- index.html
|   |-- package.json
|   |-- tsconfig.app.json
|   |-- tsconfig.json
|   |-- tsconfig.node.json
|   `-- vite.config.ts
|-- docs/
|-- prompts/
|-- tasks/
|-- docker-compose.yml
`-- .env.example
```

## Running Checks

Backend compile check:

```bash
python -m compileall backend
```

Docker Compose validation:

```bash
docker compose config
```

Database migration check:

```bash
cd backend
alembic upgrade head
```

Health check:

```bash
curl http://localhost:8000/health
```

## Notes

- No business entities are implemented in this task.
- No AI providers are configured in this task.
- No n8n integration is configured in this task.
- The desktop application layer is still intentionally excluded from the current task sequence.
