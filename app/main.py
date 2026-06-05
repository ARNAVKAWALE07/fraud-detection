from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import generate_latest
import joblib 
import pandas as pd
import time
from metrics import REQUEST_COUNT, PREDICTION_COUNT, PREDICTION_LATENCY 

app = FastAPI(title= 'Fraud Detection API')
model = joblib.load('model.pkl')

class Transaction(BaseModel):
    Time: float
    v1: float; v2: float; v3 :float; v4:float; v5:float
    v6:float; v7:float; v8:float; v9:float; v10: float
    v11:float; v12: float; v13:float; v14:float; v15: float
    v16:float; v17:float; v18: float; v19: float; v20:float
    v21:float; v22:float; v23:float; v24: float; v25:float;
    v26:float; v27:float; v28:float
    Amount: float

@app.get("/health")
def health():
    REQUEST_COUNT.labels(endpoint ="/health", status= "200").inc()
    return{"status":"healthy"}

@app.post("/predict")
def predict(transction: Transaction):
    start  = time.time()
    try:
        df = pd.DataFrame([transction.model_dump()])
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]
        
        result = "fraud" if prediction == 1 else "legit"
        PREDICTION_COUNT.labels(result= result).inc()
        REQUEST_COUNT.labels(endpoint="/predict", status= "200").inc()
        PREDICTION_LATENCY.observe(time.time()- start)

        return{
            "is_fraud": bool(prediction),
            "fraud_probability": round(float(probability), 4),
            "result": result,
            "latency_ms": round((time.time()- start)* 1000, 2)

        }
    except Exception as e:
        REQUEST_COUNT.labels(endpoint="/predict", status="500").inc()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
