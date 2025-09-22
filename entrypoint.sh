#!/usr/bin/env bash
set -e

echo "==> Aguardando banco de dados ficar acessível..."
python - <<'PY'
import os, sys, time
from sqlalchemy import create_engine
url = os.getenv("DATABASE_URL", "sqlite:///./data/easyorder.db")
for i in range(60):
    try:
        create_engine(url, pool_pre_ping=True).connect().close()
        print("DB OK")
        sys.exit(0)
    except Exception as e:
        print(f"Aguardando DB... ({i+1}/60) -> {e}")
        time.sleep(2)
sys.exit(1)
PY

echo "==> Rodando Alembic (upgrade head)..."
alembic upgrade head

if [ "${DO_SEED:-false}" = "true" ]; then
  echo "==> Rodando seed inicial..."
  python seed.py || true
fi

echo "==> Iniciando a API EasyOrder..."
exec uvicorn app.main:app --host "${UVICORN_HOST:-0.0.0.0}" --port "${UVICORN_PORT:-8000}"
