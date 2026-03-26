FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles

CMD ["sh", "-c", "until nc -z db 5432; do echo 'Waiting for DB...'; sleep 2; done && python manage.py collectstatic --noinput && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 Pinggo.asgi:application"]