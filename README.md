# ✈️ AI Travel Planner Agent – AI-Powered Trip Advisor

> An intelligent AI assistant that helps users plan their travels with smart timing suggestions, packing lists, and budget estimations — powered by Gemini and Google ADK.
---

## 🧠 Business Purpose

People often want quick, personalized travel advice — when to go, what to pack, how much it might cost.  
This agent offers:
- ✅ Travel timing suggestions
- 🎒 Packing recommendations
- 💰 Cost estimations
- 📍 Location-specific tips

Built using Gemini AI + FastAPI + Streamlit, it's perfect for:
- Solo travelers
- Travel agencies
- Chatbot integrations
- Travel bloggers or planners

---

## ⚙️ Tech Stack

| Layer           | Tool                    |
|----------------|-------------------------|
| 💬 AI Model     | Gemini 1.5 (via ADK)    |
| 🧠 Agent System | Google ADK (Agents SDK) |
| 🔧 Tools Used   | Google Search, Calculator |
| 🧪 Backend      | FastAPI                 |
| 🖥️ Frontend     | Streamlit               |
| 🔐 Auth         | Google ADC (Service Key)|
| 🐳 Deployment   | Docker + Docker Compose |


---

## 📌 Features
- 🧠 Gemini-powered responses for travel advice
- 🌐 Uses real-time tools (search, calculator)
- 🧪 FastAPI backend with `/travel-plan` endpoint
- 🖥️ Streamlit UI for interactive frontend
- 🐳 Docker + Compose setup for easy local dev

---

## 🧠 Use Case

> "What's the best time to visit Japan and what should I pack?"

The agent responds with:
- 🗓️ Best seasonal windows
- 🎒 Packing list based on weather and region
- 💰 Estimated costs using calculator tool

---

## 📂 Project Structure

```bash
AI_Travel_Agent/
├── backend/
│   ├── main.py              # FastAPI entry
│   ├── models.py            # Pydantic schemas
│   ├── routes/travel.py     # Travel route logic
│   └── services/
│       ├── ai_service.py    # Gemini agent logic
│       └── utils.py         # Text cleaner, etc
├── frontend/
│   └── app.py               # Streamlit UI
├── config/
│   ├── secrets.json         # API keys & model name
│   └── settings.py          # Env loader
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt         # All Python deps
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. 🔑 Configure Credentials
Save your Vertex AI service account key at:
```
config/vertexai-credentials.json
```
Update `config/secrets.json`:
```json
{
  "GOOGLE_APPLICATION_CREDENTIALS": "config/vertexai-credentials.json",
  "PROJECT_ID": "your-gcp-project-id",
  "DEFAULT_MODEL": "gemini-1.5-flash-latest"
}
```

---

### 2. 🧪 Run Locally (Dev Mode)
```bash
# Create venv
python -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Run FastAPI backend
uvicorn backend.main:app --reload

# In new terminal, run Streamlit
streamlit run frontend/app.py
```

---

### 3. 🐳 Run with Docker Compose
```bash
docker-compose up --build
```
- Visit FastAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Visit Streamlit: [http://localhost:8501](http://localhost:8501)

---

## 📬 API Reference

### `POST /travel-plan`
**Body:**
```json
{ "prompt": "Best time to visit Italy under $1500" }
```

**Response:**
```json
{ "response": "🇮🇹 Best time is spring or fall. Budget includes: flights, hotels..." }
```

---

## 🚀 Next Steps
- Add multi-destination support
- Integrate weather APIs
- Store user history and responses

---

## 👨‍💻 Maintainer
Built with ❤️ by Vinay.