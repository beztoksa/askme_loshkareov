FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    python3-tk \
    tk \
    cron \
    procps \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl
COPY . .
COPY crontab.txt /etc/cron.d/cache-quote-cron
RUN chmod 0644 /etc/cron.d/cache-quote-cron && \
    crontab /etc/cron.d/cache-quote-cron && \
    touch /var/log/cron.log && \
    chmod 666 /var/log/cron.log
EXPOSE 8000
