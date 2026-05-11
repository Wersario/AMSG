FROM python:3.12

WORKDIR /app

ENV PYTHONPATH=/app/backend

RUN apt-get update && apt-get install -y netcat-openbsd
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x scripts/run_dev.sh
