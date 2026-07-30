FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY idp-common /app/idp-common

RUN pip install -e /app/idp-common

COPY worker-python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker-python .

CMD ["python", "-m", "worker.main"]