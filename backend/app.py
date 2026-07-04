from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import CarInput, PredictionResponse
from model import predict_price
from utils import preprocess

app = FastAPI(
    title="Car Price Prediction API",
    description="Predicts used car prices using a CatBoost regression model.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Car Price Prediction API is running."}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(car: CarInput):
    """
    Accepts car attributes and returns the predicted market price in USD.
    """
    try:
        features = preprocess(car.model_dump())
        price = predict_price(features)
        return PredictionResponse(predicted_price=round(price, 2))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
