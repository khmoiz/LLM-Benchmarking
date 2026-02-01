FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create results dir and ensure it's writable (for bind mounts from host)
RUN mkdir -p /app/results && chmod 777 /app/results

# Copy the application
COPY app /app/app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
