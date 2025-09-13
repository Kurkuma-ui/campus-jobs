#!/bin/sh
set -e

# Накатываем миграции (если уже накатывались — Alembic просто ничего не сделает)
alembic upgrade head || true

# Сидим тестовые данные (скрипт сам проверяет, сидированы ли они)
python -m app.seed || true

# Стартуем API
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
