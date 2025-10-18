from fastapi import FastAPI
import pandas as pd
import joblib
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class request_body(BaseModel):
    tempo_na_empresa: int
    nivel_na_empresa: int

modelo_poly = joblib.load('./modelo_salario.pkl')

@app.post('/predict')
def predict(data : request_body):
    input_features = {
        'tempo_na_empresa': data.tempo_na_empresa,
        'nivel_na_empresa': data.nivel_na_empresa
    }

    pred_df = pd.DataFrame(input_features, index=[1])

    # Predição
    y_pred = modelo_poly.predict(pred_df)[0].astype(float)

    return {'salario em reais': y_pred.tolist()}