#!/usr/bin/env bash
set -euo pipefail
if [ -f .env ]; then export $(grep -v '^#' .env | xargs) ; fi
uvicorn app.main:app --reload --port 8000 