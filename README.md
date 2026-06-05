# 🔍 Real-Time Fraud Detection MLOps Pipeline

A production-grade machine learning system that detects fraudulent credit card transactions in real time. Built with a full MLOps pipeline — from experiment tracking to live deployment.

**Live API:** https://fraud-detection-production-37fa.up.railway.app/docs

---

## 🚀 What it does

- Accepts a credit card transaction as input
- Returns a fraud prediction with probability score in milliseconds
- Trained on 284,807 real anonymized transactions (Kaggle Credit Card Fraud dataset)
- Handles extreme class imbalance (only 0.17% fraud) using SMOTE oversampling

---

## 📊 Model Performance

| Model | ROC-AUC | F1 Score | Precision | Recall |
|---|---|---|---|---|
| Logistic Regression ✅ | **0.9771** | 0.77 | 1.00 | 0.55 |
| Random Forest | 0.9292 | 0.87 | 0.80 | 1.00 |
| Gradient Boosting | 0.9338 | 0.86 | 0.80 | 1.00 |

> Logistic Regression selected as best model based on ROC-AUC score.
> All experiments tracked and compared using MLflow.

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| ML Training | Scikit-learn, SMOTE (imbalanced-learn) |
| Experiment Tracking | MLflow |
| API Serving | FastAPI, Uvicorn |
| Monitoring | Prometheus client |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Deployment | Railway |
| Language | Python 3.10 |

---

## 📁 Project Structure

```
fraud-detection/
├── .github/
│   └── workflows/
│       └── cicd.yml          # GitHub Actions CI/CD pipeline
├── data/
│   └── creditcard.csv        # Kaggle dataset (not tracked in git)
├── src/
│   ├── train.py              # Model training + MLflow logging
│   ├── preprocess.py         # Feature engineering + SMOTE
│   └── producer.py           # Kafka/Redpanda transaction stream
├── app/
│   ├── main.py               # FastAPI application
│   ├── metrics.py            # Prometheus metrics
│   ├── model.pkl             # Trained model
│   └── requirements.txt      # Dependencies
├── monitoring/
│   └── prometheus.yml        # Prometheus config
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ⚙️ How to Run Locally

### Prerequisites
- Python 3.10
- Docker Desktop
- Git

### Step 1 — Clone the repo

```bash
git clone https://github.com/ARNAVKAWALE07/fraud-detection.git
cd fraud-detection
```

### Step 2 — Set up virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r app/requirements.txt
```

### Step 3 — Download dataset

Download `creditcard.csv` from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place it in the `data/` folder.

### Step 4 — Train the model

```bash
# Start MLflow server
mlflow server --host 0.0.0.0 --port 5000

# In a new terminal
cd src
python train.py
```

View experiment results at `http://localhost:5000`

### Step 5 — Run the API locally

```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8080
```

API docs at `http://127.0.0.1:8080/docs`

### Step 6 — Run with Docker

```bash
docker-compose up --build
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/predict` | POST | Predict fraud for a transaction |
| `/metrics` | GET | Prometheus metrics |
| `/docs` | GET | Interactive Swagger UI |

---

## 🧪 Sample Prediction

**Request:**
```bash
curl -X POST https://fraud-detection-production-37fa.up.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Time": 0,
    "V1": -1.35, "V2": -0.07, "V3": 2.53, "V4": 1.37, "V5": -0.33,
    "V6": 0.46, "V7": 0.23, "V8": 0.09, "V9": 0.36, "V10": 0.09,
    "V11": -0.55, "V12": -0.61, "V13": -0.99, "V14": -0.31, "V15": 1.46,
    "V16": -0.47, "V17": 0.20, "V18": 0.02, "V19": 0.40, "V20": 0.25,
    "V21": -0.01, "V22": 0.27, "V23": -0.11, "V24": 0.06, "V25": 0.12,
    "V26": -0.18, "V27": 0.13, "V28": -0.02,
    "Amount": 149.62
  }'
```

**Response:**
```json
{
  "is_fraud": false,
  "fraud_probability": 0.0017,
  "result": "legit",
  "latency_ms": 12.5
}
```

---

## 🔄 CI/CD Pipeline

Every push to `main` automatically:

1. Runs test suite with pytest
2. Builds Docker image
3. Pushes to Docker Hub
4. Railway auto-deploys the latest version

```
git push → GitHub Actions → Docker Hub → Railway → Live
```

---

## 📈 MLflow Experiment Tracking

All model experiments are tracked with:
- Hyperparameters
- ROC-AUC, F1, Precision, Recall
- Model artifacts
- Training timestamps

---

## 🧠 Key Technical Decisions

**Why SMOTE?**
Only 0.17% of transactions are fraudulent. Without oversampling, the model would predict "legit" 100% of the time and achieve 99.83% accuracy while being completely useless. SMOTE generates synthetic fraud samples to balance the training set.

**Why Logistic Regression over Random Forest?**
Logistic Regression achieved the highest ROC-AUC (0.9771) meaning it best separates fraud from legitimate transactions. In fraud detection, ranking transactions by risk score (what AUC measures) is critical for prioritizing manual review queues.

**Why FastAPI?**
FastAPI auto-generates interactive API documentation, has native async support, and is significantly faster than Flask for ML serving workloads.

---

## 📄 Dataset

[Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) — Kaggle

- 284,807 transactions
- 492 fraudulent (0.17%)
- Features V1-V28 are PCA-transformed for confidentiality
- Time and Amount are original features

---

## 👤 Author

**Arnav Kawale**
- GitHub: [@ARNAVKAWALE07](https://github.com/ARNAVKAWALE07)
- Live API: [fraud-detection-production-37fa.up.railway.app](https://fraud-detection-production-37fa.up.railway.app/docs)
- 
