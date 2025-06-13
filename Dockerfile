FROM python:3.10-slim

LABEL description="Slavbor World Backend API"

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

CMD ["/wait-for-db.sh", "db", "5432", "sh", "-c", "alembic upgrade head && python -m app.main"]