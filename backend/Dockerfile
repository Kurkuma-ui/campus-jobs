FROM python:3.12-slim

WORKDIR /app

# Ускоряем/стабилизируем pip в контейнере
ENV PIP_DEFAULT_TIMEOUT=120 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_RETRY=10

# Устанавливаем системные зависимости для psycopg и пр.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Зависимости проекта
COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --retries ${PIP_RETRY} -i https://pypi.org/simple \
       -r requirements.txt

# Копируем код
COPY . /app

# entrypoint, если используешь
# COPY entrypoint.sh /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh
# CMD ["/app/entrypoint.sh"]

# В dev-варианте — просто uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
