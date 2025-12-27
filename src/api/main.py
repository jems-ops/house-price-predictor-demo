from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from inference import predict_price, batch_predict
from schemas import HousePredictionRequest, PredictionResponse

from prometheus_client import start_http_server, Counter
import threading
import os

# Prometheus metrics
API_REQUESTS = Counter(
    "api_requests_total",
    "Total API requests",
    ["endpoint", "method", "status"]
)

def start_prometheus_server():
    """Start Prometheus metrics server on port 9100."""
    port = int(os.getenv("METRICS_PORT", 9100))  # allow override via env
    start_http_server(port)

# Initialize FastAPI app
app = FastAPI(
    title="House Price Prediction API",
    description=(
        "An API for predicting house prices based on various features. "
        "This application is part of the MLOps Bootcamp by School of Devops. "
        "Authored by Gourav Shah."
    ),
    version="1.0.0",
)

# ✅ Start metrics server safely on app startup
@app.on_event("startup")
def start_metrics():
    threading.Thread(target=start_prometheus_server, daemon=True).start()

# CORS middleware
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
    API_REQUESTS.labels("/health", "GET", "200").inc()
    return {"status": "healthy", "model_loaded": True}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: HousePredictionRequest):
    API_REQUESTS.labels("/predict", "POST", "200").inc()
    return predict_price(request)

# Batch prediction endpoint
@app.post("/batch-predict", response_model=list)
async def batch_predict_endpoint(requests: list[HousePredictionRequest]):
    API_REQUESTS.labels("/batch-predict", "POST", "200").inc()
    return batch_predict(requests)