#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
repo_root="$(cd "$skill_dir/../../.." && pwd)"
app_dir="$repo_root/Unified-Chat-Application"

if [[ ! -d "$app_dir" ]]; then
  echo "Could not find the React app directory at $app_dir" >&2
  exit 1
fi

cd "$app_dir"

if [[ ! -d node_modules ]]; then
  echo "Installing dependencies in $(pwd) ..."
  if [[ -f package-lock.json ]]; then
    npm ci
  else
    npm install
  fi
fi

npm run start
