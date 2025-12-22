# 🏠 House Price Predictor – End-to-End MLOps Pipeline

Welcome to the **House Price Predictor**! This project is a comprehensive MLOps sandbox designed to take you from raw data to a production-grade, containerized deployment.

---

## 🏗️ Project Architecture & Structure

```text
house-price-predictor/
├── configs/                # YAML-based hyperparameters & model configs
├── data/                   # Data versioning (raw vs processed)
├── deployment/
│   └── mlflow/             # Infrastructure as Code (Docker Compose for MLflow)
├── models/                 # Model Registry (serialized .pkl & preprocessors)
├── notebooks/              # EDA and rapid prototyping
├── src/                    # Modular source code
│   ├── api/                # FastAPI inference service
│   ├── data/               # Data cleaning logic
│   ├── features/           # Feature engineering pipeline
│   └── models/             # Training scripts with MLflow integration
├── streamlit_app/          # User-facing dashboard
├── requirements.txt        
└── README.md

```

---

## 🛠️ Prerequisites & Setup

Ensure your local machine has the following:

* **Core:** [Python 3.11+](https://www.python.org/), [Git](https://git-scm.com/)
* **Dev Tools:** [VS Code](https://code.visualstudio.com/), [UV (Package Manager)](https://github.com/astral-sh/uv)
* **Ops:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Podman](https://podman-desktop.io/)

### 🚀 Environment Installation

1. **Clone the Repository:**
```bash
git clone https://github.com/xxxxxx/house-price-predictor.git
cd house-price-predictor

```


2. **Initialize Virtual Environment:**
```bash
uv venv --python python3.11
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

```



---

## 📊 Experiment Tracking (MLflow)

Before training, spin up the local tracking server to visualize your experiments:

```bash
cd deployment/mlflow
docker compose -f mlflow-docker-compose.yml up -d

```

🔗 Access the dashboard at: **[http://localhost:5555](https://www.google.com/search?q=http://localhost:5555)**

---

## 🔁 The MLOps Workflow

### 1️⃣ Data Transformation

Clean raw data and generate the feature engineering pipeline.

```bash
python src/data/run_processing.py --input data/raw/house_data.csv --output data/processed/cleaned_house_data.csv
python src/features/engineer.py --input data/processed/cleaned_house_data.csv --output data/processed/featured_house_data.csv

```

### 2️⃣ Model Training & Logging

Execute the training script. This will automatically log parameters (from `configs/`) and metrics to MLflow.

```bash
python src/models/train_model.py \
  --config configs/model_config.yaml \
  --data data/processed/featured_house_data.csv \
  --mlflow-tracking-uri http://localhost:5555

```

---

## 📦 Containerization & Deployment

### Building the Services

We use a **Multi-Stage Docker Build** to keep images lean.

1. **FastAPI (Backend):** Add a `Dockerfile` in the root that installs requirements and runs `uvicorn src.api.main:app`.
2. **Streamlit (Frontend):** Add `streamlit_app/Dockerfile` to serve the UI.
3. **Orchestration:** Create a `docker-compose.yaml` in the root to link both services.

```bash
# Launch the full stack
docker compose up --build

```

### 🧪 Testing the API

Once running, you can verify the inference engine via cURL:

```bash
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "sqft": 1500, "bedrooms": 3, "bathrooms": 2, 
  "location": "suburban", "year_built": 2000, "condition": "fair"
}'

```

---

## 🎓 Learning Outcomes

* **CI/CD for ML:** Automating training with GitHub Actions.
* **Model Governance:** Versioning models and data.
* **Inference Patterns:** REST APIs vs Streamlit UI.
* **Orchestration:** Moving from Docker Compose to **ArgoCD/Kubernetes**.
