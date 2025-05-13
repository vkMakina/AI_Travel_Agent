# config/settings.py – Centralized App Configuration

import json
from pathlib import Path

# Load secrets from secrets.json
SECRETS_PATH = Path(__file__).parent / "secrets.json"

with open(SECRETS_PATH, "r") as f:
    secrets = json.load(f)

# Access values
GOOGLE_APPLICATION_CREDENTIALS = secrets.get("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = secrets.get("PROJECT_ID")
DEFAULT_MODEL = secrets.get("DEFAULT_MODEL")
LOCATION = secrets.get("LOCATION")
SERPAPI_API_KEY = secrets.get("SERPAPI_API_KEY")
GOOGLE_API_KEY = secrets.get("GOOGLE_API_KEY")

# Set ADC env var for Gemini
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(GOOGLE_APPLICATION_CREDENTIALS)
os.environ["GOOGLE_CLOUD_PROJECT"] = str(PROJECT_ID)
os.environ["GOOGLE_CLOUD_LOCATION"] = str(LOCATION)
