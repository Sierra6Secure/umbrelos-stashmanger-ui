FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask==3.0.3 gunicorn==22.0.0

#Set the working directory inside the container
RUN mkdir -p /app/data

# Copy source and frontend
COPY app/server.py .
COPY app/index.html .
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 6005

ENTRYPOINT ["/entrypoint.sh"]