# backend/routes/travel.py – Travel Planner Endpoint

from fastapi import APIRouter
from backend.models import TravelPrompt, TravelResponse
from backend.services.ai_service import run_travel_agent

router = APIRouter()

@router.post("/travel-plan", response_model=TravelResponse)
def get_travel_plan(prompt: TravelPrompt):
    response_text = run_travel_agent(prompt.prompt)
    return TravelResponse(response=response_text)
