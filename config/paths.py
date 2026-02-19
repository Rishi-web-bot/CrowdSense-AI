from pathlib import Path

# Base folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Folders
DATASETS_DIR = BASE_DIR / "datasets"
VIDEOS_DIR = DATASETS_DIR / "videos"
MODELS_DIR = BASE_DIR / "models"
ASSETS_DIR = BASE_DIR / "assets"

# Files
CSV_PATH = DATASETS_DIR / "risk_management.csv"
VIDEO1 = VIDEOS_DIR / "1.mp4"

# 🔔 Alarm sound path (THIS WAS MISSING)
ALARM_SOUND = ASSETS_DIR / "alert.mp3"

