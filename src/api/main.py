from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from inference import predict_price, batch_predict
from schemas import HousePredictionRequest, PredictionResponse

from prometheus_client import start_http_server, Counter
import threading

# Prometheus metrics
API_REQUESTS = Counter("api_requests_total", "Total API requests", ["endpoint", "method", "status"])

def start_prometheus_server():
    start_http_server(9100)  # Expose metrics on port 9100

# Start Prometheus metrics server in a separate thread
threading.Thread(target=start_prometheus_server, daemon=True).start()

# Initialize FastAPI app with metadata
app = FastAPI(
    title="House Price Prediction API",
    description=(
        "An API for predicting house prices based on various features. "
        "This application is part of the MLOps Bootcamp by School of Devops. "
        "Authored by Gourav Shah."
    ),
    version="1.0.0",
    contact={
        "name": "School of Devops",
        "url": "https://schoolofdevops.com",
        "email": "learn@schoolofdevops.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    API_REQUESTS.labels(endpoint="/health", method="GET", status="200").inc()
    return {"status": "healthy", "model_loaded": True}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: HousePredictionRequest):
    API_REQUESTS.labels(endpoint="/predict", method="POST", status="200").inc()
    return predict_price(request)

# Batch prediction endpoint
@app.post("/batch-predict", response_model=list)
async def batch_predict_endpoint(requests: list[HousePredictionRequest]):
    API_REQUESTS.labels(endpoint="/batch-predict", method="POST", status="200").inc()
    return batch_predict(requests)