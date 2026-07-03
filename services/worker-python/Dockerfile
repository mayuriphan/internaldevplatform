FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/worker-python/ .
COPY services/api-python/app ./app

CMD ["python", "-m", "worker.main"]