#!/usr/bin/env sh
set -eu

python - <<'PY'
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from app.core.config import settings

for attempt in range(1, 31):
    try:
        engine = create_engine(settings.database_url, future=True)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database is ready.")
        break
    except OperationalError:
        print(f"Waiting for database... attempt {attempt}/30")
        time.sleep(2)
else:
    raise SystemExit("Database did not become ready in time.")
PY

alembic upgrade head

exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
