#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then 
    export $(grep -v '^#' .env | xargs)
fi

uvicorn app.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000} 