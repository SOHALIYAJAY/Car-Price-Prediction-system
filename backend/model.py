import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Loaded once at import time — shared across all requests
_model = joblib.load(os.path.join(BASE_DIR, "car_price_model.pkl"))


def predict_price(processed_df) -> float:
    """Run inference and reverse the log transform applied during training."""
    log_price = _model.predict(processed_df)
    return float(np.exp(log_price[0]))
