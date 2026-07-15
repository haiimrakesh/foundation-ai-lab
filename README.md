# Foundation AI Lab

This workspace now includes a minimal FastAPI backend plus a React chat frontend for a unified agent experience.

## Architecture

See the documentation in the [docs](docs) folder:

- [docs/architecture.md](docs/architecture.md) for the overall system design
- [docs/frontend-project-overview.md](docs/frontend-project-overview.md) for the frontend overview
- [docs/backend-project-overview.md](docs/backend-project-overview.md) for the backend overview

## Backend

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the API:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

## Frontend

Install frontend dependencies:

```bash
cd Unified-Chat-Application
npm install
npm run dev
```

## Tests

Run backend tests:

```bash
pytest backend/tests
```
