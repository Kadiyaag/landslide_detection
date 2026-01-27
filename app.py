from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# -----------------------
# Load model safely
# -----------------------
bundle = joblib.load("landslide_model.pkl")
model = bundle["model"]
feature_names = bundle["features"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API is running"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        print("📥 Incoming data:", data)

        X = pd.DataFrame([data])

        # Ensure correct column order
        X = X[feature_names]

        prob = model.predict_proba(X)[0][1]
        risk_percent = round(prob * 100, 2)

        if risk_percent >= 70:
            level = "HIGH"
        elif risk_percent >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        response = {
            "landslide_risk_percent": risk_percent,
            "risk_level": level
        }

        print("📤 Response:", response)
        return jsonify(response)

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
