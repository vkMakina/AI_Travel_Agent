# backend/services/ai_apikey_service.py – Gemini Travel Planner Agent Logic (API Key version)

import datetime
import os
import traceback
from types import SimpleNamespace
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search
from config import settings
from backend.tools.expense_calculator import get_estimated_expense
from backend.tools.current_time import get_current_time
from google.adk.tools import FunctionTool

expense_tool = FunctionTool(func=get_estimated_expense)
current_time_tool = FunctionTool(func=get_current_time)


# --- Configuration ---
print("[INFO] Initializing Gemini with API Key")
os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

try:
    from google.generativeai import configure
    configure(api_key=settings.GOOGLE_API_KEY)
except Exception as e:
    print("[ERROR] Failed to configure Gemini with API Key:", e)
    raise

# --- Setup ADK Agent using model name string ---
print("[INFO] Initializing Agent with model name string (API Key mode)")
agent = Agent(
    name="TravelPlanner",
    model=settings.DEFAULT_MODEL,  # e.g., "gemini-1.5-flash"
    instruction="You are an expert travel planner. For any user query, suggest the best time to visit, what to pack, and estimate expenses. Use tools as needed.",
    tools=[expense_tool,current_time_tool],
    description="Helps users plan trips with smart suggestions."
)


# --- Session and Runner Setup ---
session_service = InMemorySessionService()
session_id = "travel_session"
try:
    session_service.create_session(app_name="TravelPlanner", user_id="demo_user", session_id=session_id)
except Exception as e:
    if "already exists" in str(e):
        print(f"[WARN] Session '{session_id}' already exists. Continuing...")
    else:
        raise

runner = Runner(agent=agent, app_name="TravelPlanner", session_service=session_service)

# --- Agent Execution Function ---
def run_travel_agent(prompt: str) -> str:
    print(f"\n--- [API KEY MODE] Running travel agent for prompt: '{prompt}' ---")
    content = SimpleNamespace(role="user", parts=[SimpleNamespace(text=prompt)])
    final_response = None
    full_response_text = ""

    try:
        events = runner.run(user_id="demo_user", session_id=session_id, new_message=content)
        for event in events:
            if event.is_final_response():
                print("[DEBUG] Event type: final_response")
            else:
                print("[DEBUG] Event type: intermediate_response")

            if hasattr(event, "is_final_response") and event.is_final_response():
                final_response = "".join(part.text for part in event.content.parts if hasattr(part, "text"))
                break
            elif hasattr(event, "is_intermediate_response") and event.is_intermediate_response():
                intermediate_text = "".join(part.text for part in event.content.parts if hasattr(part, "text"))
                full_response_text += intermediate_text

        if final_response:
            return final_response
        elif full_response_text:
            return full_response_text
        else:
            return "Error: No response received from Travel Agent."

    except Exception as e:
        print(f"[ERROR] Agent execution failed: {e}")
        traceback.print_exc()
        return f"Error during agent execution: {e}"



# --- Example Usage ---
# if __name__ == "__main__":
#     test_prompt = "Best time to visit Bali?"
#     print(run_travel_agent(test_prompt))
