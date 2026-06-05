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
    V1: float; V2: float; V3 :float; V4:float; V5:float
    V6:float; V7:float; V8:float; V9:float; V10: float
    V11:float; V12: float; V13:float; V14:float; V15: float
    V16:float; V17:float; V18: float; V19: float; V20:float
    V21:float; V22:float; V23:float; V24: float; V25:float
    V26:float; V27:float; V28:float
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
        PREDICTION_LATENCY.obserVe(time.time()- start)

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
