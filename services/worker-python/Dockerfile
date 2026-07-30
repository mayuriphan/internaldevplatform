FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY services/idp-common /app/idp-common

RUN pip install -e /app/idp-common

COPY services/worker-python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/worker-python .

CMD ["python", "-m", "worker.main"]