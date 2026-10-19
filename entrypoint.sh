#!/usr/bin/env bash
set -e

PORT="${PORT:-8000}"

if [ "$1" = "api" ]; then
    echo "Starting Market Intelligence Hub FastAPI on port ${PORT}..."
    exec uvicorn src.api.main:app --host 0.0.0.0 --port "${PORT}"
elif [ "$1" = "dbt" ]; then
    echo "Executing dbt build for target ${DBT_TARGET:-prod}..."
    cd /app/transform
    exec dbt build --profiles-dir . --target "${DBT_TARGET:-prod}"
else
    # Default to API if command starts with uvicorn or python
    if [ "$#" -eq 0 ]; then
        exec uvicorn src.api.main:app --host 0.0.0.0 --port "${PORT}"
    else
        exec "$@"
    fi
fi
