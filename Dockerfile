FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask==3.0.3 gunicorn==22.0.0

# Copy source and frontend
COPY app/server.py ./server.py
COPY app/ ./app/

# Data volume (mounted by docker-compose)
VOLUME ["/app/data"]

# Copy the entrypoint script to the root and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 6005

ENTRYPOINT ["/entrypoint.sh"]
