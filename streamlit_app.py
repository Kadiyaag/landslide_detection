import streamlit as st
import requests  # ✅ REQUIRED
import json

st.set_page_config(page_title="Landslide Risk Predictor", layout="centered")

st.title("🌍 Landslide Risk Prediction System")

# -----------------------------
# Input fields
# -----------------------------
rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=50.0)
slope = st.number_input("Slope Angle (degrees)", min_value=0.0, value=30.0)
soil_saturation = st.slider("Soil Saturation", 0.0, 1.0, 0.5)
vegetation = st.slider("Vegetation Cover", 0.0, 1.0, 0.4)
earthquake = st.selectbox("Earthquake Activity", [0, 1])
proximity = st.slider("Proximity to Water (km)", 0.0, 10.0, 2.0)

soil_type = st.selectbox("Soil Type", ["Gravel", "Sand", "Silt"])

soil_gravel = 1 if soil_type == "Gravel" else 0
soil_sand = 1 if soil_type == "Sand" else 0
soil_silt = 1 if soil_type == "Silt" else 0

# -----------------------------
# Predict button
# -----------------------------
if st.button("🔮 Predict Landslide Risk"):
    payload = {
        "Rainfall_mm": rainfall,
        "Slope_Angle": slope,
        "Soil_Saturation": soil_saturation,
        "Vegetation_Cover": vegetation,
        "Earthquake_Activity": earthquake,
        "Proximity_to_Water": proximity,
        "Soil_Type_Gravel": soil_gravel,
        "Soil_Type_Sand": soil_sand,
        "Soil_Type_Silt": soil_silt
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=payload,
            timeout=5
        )

        result = response.json()

        st.success(f"🌋 Landslide Risk: {result['landslide_risk_percent']}%")
        st.warning(f"⚠️ Risk Level: {result['risk_level']}")

    except Exception as e:
        st.error(f"❌ API Error: {e}")
