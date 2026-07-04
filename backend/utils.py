import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

_preprocessor1 = joblib.load(os.path.join(BASE_DIR, "preprocessor1.pkl"))
_preprocessor2 = joblib.load(os.path.join(BASE_DIR, "preprocessor2.pkl"))

_COLS_TO_DROP = [
    "ohe__remainder__transmission_type_CVT",
    "ohe__ipt2__fuel_type_Plug-In Hybrid",
    "ohe__remainder__transmission_type_DualClutch",
]


def preprocess(user_data: dict) -> pd.DataFrame:
    """Transform raw input dict into the feature matrix expected by the model."""
    df = pd.DataFrame([user_data])

    df = pd.DataFrame(
        _preprocessor1.transform(df),
        columns=_preprocessor1.get_feature_names_out(),
    )

    df = pd.DataFrame(
        _preprocessor2.transform(df),
        columns=_preprocessor2.get_feature_names_out(),
    )

    drop = [c for c in _COLS_TO_DROP if c in df.columns]
    df.drop(columns=drop, inplace=True)

    return df
