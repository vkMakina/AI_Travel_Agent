# backend/main.py – FastAPI Application Entry Point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import travel

app = FastAPI(title="AI Travel Planner Agent", version="1.0")

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(travel.router)

@app.get("/")
def root():
    return {"message": "Welcome to the AI Travel Planner API"}
