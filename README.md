# CalAI

AI-powered calibration and diagnostics intelligence platform for automotive engineers.

## MVP Status

This repository now contains an initial MVP implementation with:

- FastAPI backend APIs for authentication, licensing status, document upload/indexing, EHB parsing, chat, signal dependencies, and diagnostics context.
- Next.js + TypeScript + Material UI frontend dashboard for login, upload, chat, signal explorer, and diagnostics explorer.
- Docker Compose stack with frontend, backend, PostgreSQL, Qdrant, AI service placeholder, and license service placeholder.

## Setup

### 1) Backend

```bash
cd /home/runner/work/CalAI/CalAI/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd /home/runner/work/CalAI/CalAI/frontend
npm install
npm run dev
```

### 3) Full stack with Docker Compose

```bash
cd /home/runner/work/CalAI/CalAI
docker compose up --build
```

Frontend: `http://localhost:3000`  
Backend API docs: `http://localhost:8000/docs`

## Documentation

- Full project specification: `/home/runner/work/CalAI/CalAI/docs/PROJECT_SPECIFICATION.md`

## `.gitignore` Setup Guidance

A repository-level `.gitignore` is included at `/home/runner/work/CalAI/CalAI/.gitignore`.

If you need to extend it, add entries for local secrets and generated artifacts before committing.
