# Mobile Price Classification with Docker

This project implements a logistic regression model for mobile phone price classification, served as a REST API and containerized using Docker.

## Project Overview

The project accomplishes the following:

1. **Price Classification**: Predicts the price category of mobile phones based on their features
2. **Model Serving**: Implements a RESTful API using FastAPI to serve the trained logistic regression model
3. **Containerization**: Packages the application with Docker for consistent deployment
4. **Orchestration**: Uses Docker Compose for easy deployment with a single command

## Dataset

The model is trained on a dataset of mobile phone features and their corresponding price categories:

- **Features**: Battery power, Bluetooth, clock speed, dual SIM, camera specs, memory, dimensions, etc.
- **Target**: Price category (0: Low Cost, 1: Medium Cost, 2: High Cost, 3: Very High Cost)

## Prerequisites

- Docker and Docker Compose
- Git (to clone the repository)

## Quick Start

To deploy the application:

```bash
# Clone the repository
git clone https://github.com/yourusername/mobile-price-classification.git
cd mobile-price-classification

# Start the services using Docker Compose
docker-compose up -d
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the service is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

- `POST /predict`: Submit a mobile phone's features for price category prediction
  - Request: JSON with mobile phone features
  - Response: JSON with predicted price category and confidence scores

- `POST /predict_batch`: Submit multiple phones for batch prediction
  - Request: JSON array of mobile phone features
  - Response: JSON array with predicted categories and confidence scores for each phone

- `GET /health`: Check if the service is running
  - Response: JSON with service status

## Testing the API

Use the provided `test_api.py` script to test the API:

```bash
# Test single prediction with randomly generated mobile features
python test_api.py --url http://localhost:8000

# Test batch prediction
python test_api.py --url http://localhost:8000 --batch --batch-size 10
```
## Development Setup

For local development:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application locally
uvicorn app.main:app --reload
```

## Troubleshooting

Common issues and solutions:

1. **Model loading error**: Ensure the model path is correctly specified in docker-compose.yml
2. **Memory issues**: Adjust container memory limits in docker-compose.yml
3. **Connection refused**: Check if the container is running and ports are correctly mapped

## Docker Hub

The Docker image is available on Docker Hub:

```bash
docker pull andt123/mobile-price-api:latest
```

## Video Demonstration

[Model API Deployment with Docker Demo](https://youtu.be/Rq1_2sQYOmU)

This video demonstrates:
1. Building the Docker image
2. Deploying with Docker Compose
3. Making API requests
4. Viewing the results 