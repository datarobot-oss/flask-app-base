#!/usr/bin/env bash
echo "Starting App"

export token="$DATAROBOT_API_TOKEN"
export endpoint="$DATAROBOT_ENDPOINT"

gunicorn -b :8080 flask_app:flask_app  --timeout 200 --graceful-timeout 30