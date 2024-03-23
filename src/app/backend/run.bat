@echo off
start cmd /k uvicorn main:create_app --host 0.0.0.0 --port 8000 --reload --log-level debug
start cmd /k celery -A task.worker worker -E -P threads --concurrency=2