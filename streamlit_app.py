import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="AI Landslide Management System",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# HEADER
# ===============================
st.markdown("""
<div style="background:linear-gradient(135deg,#7c2d12,#ea580c);
padding:2rem;border-radius:12px;">
<h1 style="color:white;text-align:center;">🌋 AI-Powered Landslide Management System</h1>
<p style="color:#fed7aa;text-align:center;">
Real-time Landslide Risk Assessment & Emergency Coordination
</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR INPUTS
# ===============================
with st.sidebar:
    st.header("🎯 Landslide Risk Parameters")
    st.markdown("---")

    rainfall = st.slider("🌧️ Rainfall (mm)", 0, 300, 120)
    slope = st.slider("⛰️ Slope Angle (°)", 0, 90, 35)
    soil_saturation = st.slider("💧 Soil Saturation", 0.0, 1.0, 0.65)
    vegetation = st.slider("🌱 Vegetation Cover", 0.0, 1.0, 0.4)
    earthquake = st.selectbox("🌐 Earthquake Activity", [0, 1])
    proximity = st.slider("🚰 Distance to Water (km)", 0.0, 10.0, 1.5)

    soil_type = st.selectbox("🪨 Soil Type", ["Gravel", "Sand", "Silt"])

    analyze = st.button("🔍 Analyze Landslide Risk", type="primary", use_container_width=True)

# One-hot soil encoding
soil_gravel = 1 if soil_type == "Gravel" else 0
soil_sand = 1 if soil_type == "Sand" else 0
soil_silt = 1 if soil_type == "Silt" else 0

features = {
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

# ===============================
# API CALL
# ===============================
def get_prediction(data):
    try:
        res = requests.post(
            "http://127.0.0.1:5000/predict",
            json=data,
            timeout=5
        )
        return res.json()
    except:
        return None

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if analyze:
    with st.spinner("🧠 AI analyzing landslide risk..."):
        st.session_state.prediction = get_prediction(features)

prediction = st.session_state.prediction

# ===============================
# MAIN DASHBOARD
# ===============================
if prediction:
    risk = prediction["landslide_risk_percent"]
    level = prediction["risk_level"]

    col1, col2, col3 = st.columns(3)

    col1.metric("🌋 Landslide Risk", f"{risk} %")
    col2.metric("⚠️ Risk Level", level)
    col3.metric("🕒 Last Updated", datetime.now().strftime("%H:%M"))

    if level == "HIGH":
        st.error("🚨 CRITICAL LANDSLIDE WARNING – Immediate evacuation required")
    elif level == "MEDIUM":
        st.warning("⚠️ MODERATE RISK – Continuous monitoring advised")
    else:
        st.success("✅ LOW RISK – Conditions stable")

# ===============================
# ZONE-WISE RISK
# ===============================
st.header("🗺️ Zone-Wise Landslide Risk")

zones = pd.DataFrame([
    {"Zone": "Hill Slope A", "Risk": "HIGH", "Action": "Evacuate", "Authority": "District Collector"},
    {"Zone": "Valley B", "Risk": "MEDIUM", "Action": "Restrict Movement", "Authority": "Police"},
    {"Zone": "Forest C", "Risk": "MEDIUM", "Action": "Monitoring", "Authority": "Forest Dept"},
    {"Zone": "Town D", "Risk": "LOW", "Action": "Normal Watch", "Authority": "Municipality"},
])

fig = go.Figure(go.Bar(
    x=zones["Zone"],
    y=[80, 60, 55, 30],
    text=zones["Risk"],
    marker_color=["#dc2626", "#ea580c", "#ea580c", "#16a34a"]
))

fig.update_layout(
    title="Landslide Risk by Zone",
    yaxis_title="Risk Severity",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# GOVERNMENT ACTIONS
# ===============================
st.header("⚡ AI-Triggered Emergency Actions")

actions = [
    "Slope stabilization teams deployed",
    "Heavy vehicle movement restricted",
    "Rainfall sensors activated",
    "Evacuation shelters prepared",
    "Geological survey teams alerted"
]

for act in actions:
    st.success(f"✔ {act}")

# ===============================
# FOOTER ALERT
# ===============================
st.info("🔔 AI system continuously monitors rainfall, slope stability, and seismic activity")
