# 🚗 Car Price Prediction

A full-stack machine learning web application that predicts used car prices using a **CatBoostRegressor** model.

## Tech Stack

| Layer    | Technology          |
|----------|---------------------|
| Backend  | FastAPI + Uvicorn   |
| Frontend | Streamlit           |
| Model    | CatBoostRegressor   |

## Project Structure

```
car-price-prediction/
├── backend/
│   ├── app.py              # FastAPI application & routes
│   ├── model.py            # Model loading & inference
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── utils.py            # Preprocessing pipeline
│   ├── car_price_model.pkl
│   ├── preprocessor1.pkl
│   ├── preprocessor2.pkl
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Setup & Run

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Frontend available at: http://localhost:8501

## Model Details

- **Algorithm:** CatBoostRegressor
- **R² Score:** 0.92
- **Target:** Log-transformed price (reversed with `np.exp` at inference)
- **Dataset Size:** ~50,000 records

## Input Fields

| Field             | Type   | Constraints                        |
|-------------------|--------|------------------------------------|
| Brand             | string | Required                           |
| Model             | string | Required                           |
| Model Year        | int    | 1990 – current year                |
| Mileage           | float  | > 0                                |
| Fuel Type         | string | Gasoline / Diesel / Hybrid / etc.  |
| Accident History  | string | None reported / At least 1...      |
| Transmission Type | string | Automatic / Manual / CVT / etc.    |
| Horsepower        | float  | > 0                                |
| Engine Size (L)   | float  | > 0                                |
| Cylinders         | float  | 2 – 16                             |
