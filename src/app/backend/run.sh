#!/bin/bash

# Starts the fastapi server
uvicorn main:create_app --host 0.0.0.0 --port 8000 --reload --log-level 'debug' &

# Starts the celery worker for the prediction task
celery -A task.worker worker --concurrency=1 -E -P threads &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?