#!/bin/bash

uvicorn main:create_app --host 0.0.0.0 --port 8000 --reload --log-level 'debug' &
celery --app=task.worker worker -E -P threads --concurrency=2 &

tail -f /dev/null