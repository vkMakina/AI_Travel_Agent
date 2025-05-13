import os
from google.cloud import aiplatform

# === Set Your ADC Credentials ===
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Test\\Documents\\adk_poc\\vertexai-tutorial-454518-595d95d2c310.json"

# === Replace with your actual values ===
PROJECT_ID = "vertexai-tutorial-454518"
LOCATION = "us-central1"

# === Initialize Vertex AI client ===
aiplatform.init(project=PROJECT_ID, location=LOCATION)

# === List available models ===
try:
    models = aiplatform.Model.list()
    print(f"✅ SUCCESS: Found {len(models)} models in project.")
    for model in models[:3]:  # Print first 3 models for preview
        print(f"Model Name: {model.display_name}")
except Exception as e:
    print("❌ ERROR: Failed to connect to Vertex AI")
    print(str(e))
