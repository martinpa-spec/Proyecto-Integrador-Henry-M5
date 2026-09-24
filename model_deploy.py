import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union

app = FastAPI(
    title="CrediPulse - API de Predicción",
    description="Endpoint para predicciones por lotes (batch) de riesgo crediticio",
    version="1.0.0"
)

# Cargar el modelo entrenado
try:
    model = joblib.load("modelo_credipulse.pkl")
except Exception:
    model = None

class ClienteData(BaseModel):
    capital_prestado: float
    salario_cliente: float
    cuota_pactada: float
    edad_cliente: int
    tipo_laboral: str
    tendencia_ingresos: str

@app.get("/")
def home():
    return {"status": "OK", "message": "API CrediPulse operando correctamente"}

@app.post("/predict")
def predict(data: Union[ClienteData, List[ClienteData]]):
    """Endpoint /predict que acepta registros individuales o por lotes (batch)."""
    if model is None:
        raise HTTPException(status_code=500, detail="El modelo (.pkl) no fue encontrado.")
    
    if isinstance(data, ClienteData):
        data = [data]
        
    df = pd.DataFrame([item.dict() for item in data])
    predictions = model.predict(df).tolist()
    
    return {
        "cantidad_registros": len(predictions),
        "predicciones": predictions
    }