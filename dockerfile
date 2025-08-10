FROM python:3.9-slim

WORKDIR /app
RUN apt-get update && apt-get install -y \
    supervisor \
    && rm -rf /var/lib/apt/lists/*
# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .
# Create supervisor configuration
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports 
EXPOSE 8000 8501

# Create startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Run both services
CMD ["/app/start.sh"]