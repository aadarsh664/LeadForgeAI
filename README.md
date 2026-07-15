# LeadForgeAI

LeadForgeAI is a local-first Lead Intelligence Platform designed to help users discover, enrich, analyze, and organize business leads through a desktop-oriented experience.

This repository is currently bootstrapped for `TASK-001`, which establishes the foundational backend and frontend applications without business features, database integration, AI, or workflow automation.

## Current Scope

- FastAPI backend bootstrap
- React + TypeScript + Vite frontend bootstrap
- Health check integration between frontend and backend
- Docker Compose development setup
- Environment variable template

## Requirements

- Python 3.13
- Node.js 22 or newer
- npm 11 or newer
- Docker Desktop with Docker Compose support

## Installation

1. Copy `.env.example` to `.env`.
2. Install backend dependencies:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Development

### Run the backend

```bash
cd backend
.venv\Scripts\activate
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

Start both applications with Docker Compose:

```bash
docker compose up --build
```

The compose setup is ready for future PostgreSQL and Redis services but does not include them yet.

## Available Endpoints

- `GET /health`
- `GET /api/v1/health`

Example response:

```json
{
  "success": true,
  "status": "healthy",
  "application": "LeadForgeAI"
}
```

## Folder Structure

```text
LeadForgeAI/
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |-- core/
|   |   |-- models/
|   |   |-- repositories/
|   |   |-- schemas/
|   |   |-- services/
|   |   |-- utils/
|   |   `-- main.py
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

Backend health check:

```bash
curl http://localhost:8000/health
```

Frontend health check:

1. Open the frontend in a browser.
2. Click `Health Check`.
3. Confirm the backend status updates to `Healthy`.

## Notes

- No database is configured in this task.
- No AI providers are configured in this task.
- No workflow engine is configured in this task.
- The desktop application layer is intentionally excluded from `TASK-001`.
