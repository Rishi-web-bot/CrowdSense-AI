import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "datasets" / "risk_management.csv"
MODELS_DIR = BASE_DIR / "models"

MODELS_DIR.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(CSV_PATH)

# Convert text location to numbers
le = LabelEncoder()
df["location"] = le.fit_transform(df["location"])

# Split features & target
X = df.drop("risk", axis=1)
y = df["risk"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = RandomForestClassifier()
model.fit(X_scaled, y)

# Save files
joblib.dump(model, MODELS_DIR / "risk_model.pkl")
joblib.dump(scaler, MODELS_DIR / "scaler.pkl")

print("✅ Risk model trained and saved!")
