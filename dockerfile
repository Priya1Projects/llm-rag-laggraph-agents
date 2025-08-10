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

# Install tini for process management (optional)
RUN apt-get update && apt-get install -y tini
# Expose ports 
EXPOSE 7860  8000 8501

# Run both services
CMD ["sh", "-c", "tini -- uvicorn src.api.main:app --host 0.0.0.0 --port 8000 & streamlit run src/frontend/app.py --server.port 8501 --server.address 0.0.0.0"]