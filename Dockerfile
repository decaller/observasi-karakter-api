FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc libcairo2 && rm -rf /var/lib/apt/lists/*

COPY observasi-karakter-core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY observasi-karakter-core .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
