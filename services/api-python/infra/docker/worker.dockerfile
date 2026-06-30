FROM python:3.11-slim

WORKDIR /worker

COPY services/worker-python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/worker-python .

ENV PYTHONPATH=/worker

CMD ["python", "main.py"]