#!/usr/bin/env bash
set -euo pipefail

echo "Starting App"

# Default to 4 workers — nproc is unreliable in containers because it reports
# the host CPU count, not the container's CPU limit, causing runaway worker
# counts and OOM kills. Override via GUNICORN_WORKERS if needed.
WORKERS=${GUNICORN_WORKERS:-4}

exec gunicorn flask_app:flask_app \
  --bind :8080 \
  --workers "${WORKERS}" \
  --timeout 200 \
  --graceful-timeout 30 \
  --access-logfile - \
  --error-logfile -
