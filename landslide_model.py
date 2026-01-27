import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ===============================
# 1. LOAD DATASET
# ===============================
DATA_PATH = "data/landslide_dataset.csv"
TARGET_COLUMN = "Landslide"

df = pd.read_csv(DATA_PATH)

print("✅ Dataset loaded successfully")
print(df.head())
print("\nColumns:", list(df.columns))

# ===============================
# 2. SPLIT FEATURES & TARGET
# ===============================
X = df.drop(TARGET_COLUMN, axis=1)
y = df[TARGET_COLUMN]

# ===============================
# 3. TRAIN-TEST SPLIT
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# ===============================
# 4. TRAIN MODEL
# ===============================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ===============================
# 5. EVALUATION
# ===============================
y_pred = model.predict(X_test)

print("\n🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# ===============================
# 6. PROBABILITY-BASED RISK
# ===============================
print("\n🔮 Sample Risk Predictions:")

risk_probs = model.predict_proba(X_test)

def risk_level(prob):
    if prob < 0.3:
        return "LOW"
    elif prob < 0.6:
        return "MEDIUM"
    else:
        return "HIGH"

for i in range(5):
    prob = risk_probs[i][1]  # Probability of Landslide = 1
    print(
        f"Sample {i}: "
        f"Risk = {prob*100:.2f}% | "
        f"Level = {risk_level(prob)}"
    )

# ===============================
# 7. REAL-WORLD PREDICTION (NEW AREA)
# ===============================
# ⚠️ Order MUST match dataset columns (except target)

new_area = [[
    250,   # Rainfall_mm
    42,    # Slope_Angle
    0.85,  # Soil_Saturation
    0.25,  # Vegetation_Cover
    1,     # Earthquake_Activity
    0.10,  # Proximity_to_Water
    0,     # Soil_Type_Gravel
    1,     # Soil_Type_Sand
    0      # Soil_Type_Silt
]]

new_prob = model.predict_proba(new_area)[0][1]

print("\n🌍 New Area Prediction")
print(f"Landslide Risk: {new_prob*100:.2f}%")
print(f"Risk Level: {risk_level(new_prob)}")

# ===============================
# 8. SAVE MODEL
# ===============================
# Save model + feature names together
joblib.dump(
    {
        "model": model,
        "features": list(X.columns)
    },
    "landslide_model.pkl"
)

print("💾 Model & feature names saved")
