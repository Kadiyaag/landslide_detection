from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL BUNDLE
# =========================
bundle = joblib.load("landslide_model.pkl")

model = bundle["model"]
feature_names = bundle["features"]
scaler = bundle.get("scaler", None)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Landslide API running"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        # -------------------------
        # Convert input
        # -------------------------
        X = pd.DataFrame([data])
        X = X[feature_names]

        # -------------------------
        # Apply scaling (CRITICAL)
        # -------------------------
        if scaler is not None:
            X_scaled = scaler.transform(X)
        else:
            X_scaled = X.values

        # -------------------------
        # ML probability
        # -------------------------
        ml_prob = model.predict_proba(X_scaled)[0][1]

        # -------------------------
        # RISK AMPLIFICATION LOGIC
        # -------------------------
        rainfall = data["Rainfall_mm"]
        slope = data["Slope_Angle"]
        saturation = data["Soil_Saturation"]
        vegetation = data["Vegetation_Cover"]
        proximity = data["Proximity_to_Water"]

        rule_score = 0

        if rainfall > 150:
            rule_score += 0.15
        if rainfall > 300:
            rule_score += 0.25

        if slope > 35:
            rule_score += 0.15
        if slope > 60:
            rule_score += 0.25

        if saturation > 0.6:
            rule_score += 0.15
        if saturation > 0.85:
            rule_score += 0.25

        if vegetation < 0.3:
            rule_score += 0.1

        if proximity < 2:
            rule_score += 0.1

        # -------------------------
        # FINAL RISK SCORE
        # -------------------------
        final_prob = ml_prob + rule_score
        final_prob = min(final_prob, 0.99)

        risk_percent = round(final_prob * 100, 2)

        # -------------------------
        # Risk levels
        # -------------------------
        if risk_percent >= 70:
            level = "HIGH"
        elif risk_percent >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        return jsonify({
            "landslide_risk_percent": risk_percent,
            "risk_level": level
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
