FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and data
COPY src/app.py .
COPY src/game_data.json .

# Set environment variables
ENV PORT=8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"] 