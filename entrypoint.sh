#!/bin/bash

# Database migration
poetry run alembic upgrade head

# Start the FastAPI application
poetry run fastapi run user_todo_api/app.py --host 0.0.0.0