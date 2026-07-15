#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
repo_root="$(cd "$skill_dir/../../.." && pwd)"
backend_dir="$repo_root/Unified-Agent-Backend"
frontend_dir="$repo_root/Unified-Chat-Application"

if [[ ! -d "$backend_dir" ]]; then
  echo "Could not find backend directory at $backend_dir" >&2
  exit 1
fi

if [[ ! -d "$frontend_dir" ]]; then
  echo "Could not find frontend directory at $frontend_dir" >&2
  exit 1
fi

if [[ ! -d "$frontend_dir/node_modules" ]]; then
  echo "Installing frontend dependencies in $frontend_dir ..."
  cd "$frontend_dir"
  if [[ -f package-lock.json ]]; then
    npm ci
  else
    npm install
  fi
fi

python -m pip install -r "$repo_root/requirements.txt" >/dev/null 2>&1 || true

cleanup() {
  if [[ -n "${backend_pid:-}" ]]; then
    kill "$backend_pid" 2>/dev/null || true
  fi
  if [[ -n "${frontend_pid:-}" ]]; then
    kill "$frontend_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

cd "$backend_dir"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
backend_pid=$!

cd "$frontend_dir"
npm run dev -- --host 127.0.0.1 --port 5173 &
frontend_pid=$!

wait "$backend_pid" "$frontend_pid"
