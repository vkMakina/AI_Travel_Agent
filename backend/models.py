# backend/models.py – Pydantic Schemas

from pydantic import BaseModel

class TravelPrompt(BaseModel):
    prompt: str

class TravelResponse(BaseModel):
    response: str
