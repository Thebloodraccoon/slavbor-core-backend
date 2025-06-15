FROM python:3.10.13-slim AS builder

LABEL description="Slavbor World Backend API"

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip wheel --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.10.13-slim

LABEL description="Slavbor World Backend API"

RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN useradd --create-home --shell /bin/bash --uid 1000 app \
    && chown -R app:app /app

COPY --from=builder /wheels /wheels
COPY requirements.txt .

RUN pip install --no-deps --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

COPY --chown=app:app . .
USER app

ENTRYPOINT ["sh", "-c"]
CMD ["sleep 15 && alembic upgrade head && python -m app.main"]
