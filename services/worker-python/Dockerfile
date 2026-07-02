FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker-python .
COPY api-python/app ./app

CMD ["python", "-m", "worker.main"]