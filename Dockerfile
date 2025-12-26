FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (better caching & correctness)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code AFTER deps
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]