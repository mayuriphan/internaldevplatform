FROM python:3.11-slim

WORKDIR /app

COPY services/idp-common /app/idp-common

RUN pip install -e /app/idp-common

COPY services/api-python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/api-python .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]