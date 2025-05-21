FROM python:3.10-slim

WORKDIR /app

# Copy and install dependencies first
# This layer will be cached unless requirements.txt changes
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app/main.py
ENV PORT=8000
ENV HOST=0.0.0.0
ENV MODEL_PATH=/app/models/Logistic_Model.pkl

# Copy models directory
COPY models/ /app/models/

# Copy application code last
# This way, code changes don't invalidate the dependency cache
COPY app/ /app/app/

# Expose port for API
EXPOSE 8000

# Run API server
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
