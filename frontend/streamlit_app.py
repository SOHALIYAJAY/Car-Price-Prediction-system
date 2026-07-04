import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000/predict"
CURRENT_YEAR = datetime.now().year

st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

st.markdown(
    """
    <style>
        .main { background-color: #ffffff; }
        h1 { color: #1a73e8; }
        .stButton>button {
            background-color: #1a73e8;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-size: 1rem;
        }
        .stButton>button:hover { background-color: #1558b0; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("ℹ️ Project Info")
    st.markdown("**Car Price Prediction**")
    st.markdown("Estimates the market value of a used car based on its attributes.")
    st.divider()
    st.markdown("🤖 **Model:** CatBoostRegressor")
    st.markdown("📊 **R² Score:** 0.92")
    st.divider()
    st.caption("Built with FastAPI + Streamlit")

st.title("🚗 Car Price Predictor")
st.markdown("Fill in the car details below and click **Predict Price** to get an instant estimate.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    brand = st.text_input("Brand", placeholder="e.g. Toyota")
    car_model = st.text_input("Model", placeholder="e.g. Camry")
    model_year = st.number_input("Model Year", min_value=1990, max_value=CURRENT_YEAR, value=2020, step=1)
    mileage = st.number_input("Mileage (miles)", min_value=1, value=30000, step=500)
    fuel_type = st.text_input("Fuel Type", placeholder="Example: Gasoline")
    st.markdown('<p style="font-size:12px;color:#9CA3AF;margin-top:4px;line-height:1.6;">Supported values: Gasoline • Hybrid • Diesel • E85 Flex Fuel • Plug-In Hybrid • etc.</p>', unsafe_allow_html=True)

with col2:
    accident = st.selectbox("Accident History", ["None reported", "At least 1 accident or damage reported"])
    transmission = st.text_input("Transmission Type", placeholder="Example: Automatic")
    st.markdown('<p style="font-size:12px;color:#9CA3AF;margin-top:4px;line-height:1.6;">Supported values: Automatic • Manual • CVT • DualClutch • etc.</p>', unsafe_allow_html=True)
    horsepower = st.number_input("Horsepower (HP)", min_value=1, value=150, step=5)
    engine_size = st.number_input("Engine Size (L)", min_value=0.1, value=2.0, step=0.1, format="%.1f")
    cylinder = st.number_input("Cylinders", min_value=2, max_value=16, value=4, step=1)

st.divider()

def validate_inputs():
    errors = []
    if not brand.strip():
        errors.append("Brand is required.")
    if not car_model.strip():
        errors.append("Model is required.")
    if not fuel_type.strip():
        errors.append("Fuel Type is required.")
    if not transmission.strip():
        errors.append("Transmission Type is required.")
    if not (1990 <= model_year <= CURRENT_YEAR):
        errors.append(f"Model year must be between 1990 and {CURRENT_YEAR}.")
    if mileage <= 0:
        errors.append("Mileage must be positive.")
    if horsepower <= 0:
        errors.append("Horsepower must be positive.")
    if engine_size <= 0:
        errors.append("Engine size must be positive.")
    if not (2 <= cylinder <= 16):
        errors.append("Cylinders must be between 2 and 16.")
    return errors

if st.button("🔍 Predict Price"):
    errors = validate_inputs()

    if errors:
        for err in errors:
            st.error(err)
    else:
        payload = {
            "brand": brand.strip(),
            "model": car_model.strip(),
            "model_year": int(model_year),
            "milage_ml": float(mileage),
            "fuel_type": fuel_type,
            "accident": accident,
            "transmission_type": transmission,
            "HP": float(horsepower),
            "Engine_L": float(engine_size),
            "Cylinder": float(cylinder),
        }

        with st.spinner("Predicting..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    price = response.json()["predicted_price"]
                    st.success(f"💰 Estimated Price: **${price:,.2f} USD**")
                elif response.status_code == 422:
                    detail = response.json().get("detail", "Invalid input.")
                    st.error(f"Validation error: {detail}")
                else:
                    st.error(f"Server error ({response.status_code}). Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the backend. Make sure the FastAPI server is running on port 8000.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
