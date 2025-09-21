#!/bin/sh

echo "Executando migrações do Alembic..."
alembic upgrade head

echo "Populando banco de dados inicial..."
python seed.py

echo "Iniciando a API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
