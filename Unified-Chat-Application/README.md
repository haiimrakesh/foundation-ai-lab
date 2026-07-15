# Unified Chat Application

A Vite + React chat UI for the Foundation AI Lab backend.

## Run locally

```bash
npm install
npm run dev
```

The app expects the FastAPI backend to be running at http://localhost:8000.

By default, the frontend calls `/api/*` and Vite proxies those requests to `http://127.0.0.1:8000` during development.
You can override the API base URL with `VITE_API_BASE_URL` when needed (for example, a remote backend URL).
