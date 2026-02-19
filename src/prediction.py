import pandas as pd
from config.paths import DATASETS_DIR

data = pd.read_csv(DATASETS_DIR / "risk_management.csv")

def predict_risk(input_data):

    latitude = input_data[0]
    longitude = input_data[1]

    data["distance"] = (
        (data["latitude"] - latitude)**2 +
        (data["longitude"] - longitude)**2
    )

    nearest = data.loc[data["distance"].idxmin()]

    return {
        "location": nearest["location"],
        "temperature": nearest["temperature"],
        "risk": nearest["risk"]
    }
