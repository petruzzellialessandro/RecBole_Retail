#!/bin/bash

uvicorn main:create_app --host 0.0.0.0 --port 8000 --reload --log-level 'debug' &
celery -A task.worker worker --concurrency=1 -E -P threads &

tail -f /dev/null