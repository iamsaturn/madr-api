#!/bin/sh
alembic upgrade head
fastapi run madr_api/app.py --host 0.0.0.0 --port 8000