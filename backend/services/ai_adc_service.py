# backend/services/ai_service.py – Gemini Travel Planner Agent Logic

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search
# from google.genai import client as genai_client # Keep this import if needed elsewhere, but genai is often imported as google.generativeai
import google.generativeai as genai # Use this consistent import style
import vertexai # Import the Vertex AI client library
from types import SimpleNamespace
from config import settings
import google.auth
import os
import asyncio # Import asyncio - good practice although runner uses its own thread
import traceback # Import traceback for better error logging
import sys # Import sys to check Python version if needed

print(f"Python version: {sys.version}") # Debugging: print Python version

# --- Environment and Auth Setup ---
# 1. Load ADC first - This confirms credentials are findable
try:
    creds, adc_project_id = google.auth.default()
    print(f"ADC credentials loaded successfully. ADC Project ID: {adc_project_id}")
    # Note: settings.PROJECT_ID should ideally match adc_project_id or be the one you intend to use.
    if adc_project_id and settings.PROJECT_ID != adc_project_id:
        print(f"WARNING: Configured PROJECT_ID ({settings.PROJECT_ID}) differs from ADC Project ID ({adc_project_id}). Using configured PROJECT_ID.")

except Exception as e:
    print(f"Error loading ADC credentials: {e}")
    print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set correctly")
    print("and the service account key file exists and is accessible, or you are authenticated via gcloud.")
    raise # Fatal error if credentials can't be loaded

# 2. Set Environment Variables *before* initializing any ADK components
# These are crucial for the ADK Agent/Client and underlying genai/Vertex AI libraries
print(f"[DEBUG] Setting GOOGLE_APPLICATION_CREDENTIALS from settings: {settings.GOOGLE_APPLICATION_CREDENTIALS}")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS

# Set ADK-specific Vertex env vars (might still be needed by ADK itself)
print(f"[DEBUG] Setting GOOGLE_VERTEXAI_PROJECT from settings: {settings.PROJECT_ID}")
os.environ["GOOGLE_VERTEXAI_PROJECT"] = settings.PROJECT_ID

print(f"[DEBUG] Setting GOOGLE_VERTEXAI_LOCATION from settings: {settings.LOCATION}")
os.environ["GOOGLE_VERTEXAI_LOCATION"] = settings.LOCATION

# *** ADD comprehensive standard google-generativeai env vars for Vertex AI ***
# These are the variables the underlying google.genai.Client constructor often looks for.
# Setting multiple might work around issues with specific variable names being checked,
# especially in different threading contexts.
print(f"[DEBUG] Setting GOOGLE_CLOUD_PROJECT (genai): {settings.PROJECT_ID}")
os.environ["GOOGLE_CLOUD_PROJECT"] = settings.PROJECT_ID
print(f"[DEBUG] Setting GCLOUD_PROJECT (genai): {settings.PROJECT_ID}")
os.environ["GCLOUD_PROJECT"] = settings.PROJECT_ID
print(f"[DEBUG] Setting CLOUD_ML_PROJECT_ID (genai): {settings.PROJECT_ID}")
os.environ["CLOUD_ML_PROJECT_ID"] = settings.PROJECT_ID

print(f"[DEBUG] Setting GOOGLE_CLOUD_LOCATION (genai): {settings.LOCATION}")
os.environ["GOOGLE_CLOUD_LOCATION"] = settings.LOCATION
print(f"[DEBUG] Setting GOOGLE_CLOUD_REGION (genai): {settings.LOCATION}") # Region is often used interchangeably with location
os.environ["GOOGLE_CLOUD_REGION"] = settings.LOCATION
print(f"[DEBUG] Setting CLOUD_ML_REGION (genai): {settings.LOCATION}")
os.environ["CLOUD_ML_REGION"] = settings.LOCATION
print(f"[DEBUG] Setting LOCATION (genai): {settings.LOCATION}")
os.environ["LOCATION"] = settings.LOCATION

# Explicitly ensure API key is NOT set if you are using ADC/Vertex AI
# Having both can cause authentication conflicts.
print("[DEBUG] Explicitly disabling API Key mode by setting GOOGLE_API_KEY=''")
os.environ["GOOGLE_API_KEY"] = ""


# *** Explicitly initialize Vertex AI client library ***
# This might set up necessary internal state that the google.generativeai
# client created by ADK can leverage in the threaded environment.
print(f"[DEBUG] Initializing vertexai client with project={settings.PROJECT_ID}, location={settings.LOCATION}")
try:
    vertexai.init(project=settings.PROJECT_ID, location=settings.LOCATION)
    print("vertexai client initialized successfully.")
except Exception as e:
    print(f"WARNING: Error initializing vertexai client: {e}")
    print("Continuing, but this might be related to the downstream error.")
    # Decide if this should be a fatal error in your app


# --- Verify Environment Variables are Set ---
print("\n--- Verifying Environment Variables ---")
print(f"GOOGLE_APPLICATION_CREDENTIALS in ENV: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")
print(f"GOOGLE_VERTEXAI_PROJECT in ENV: {os.environ.get('GOOGLE_VERTEXAI_PROJECT')}")
print(f"GOOGLE_VERTEXAI_LOCATION in ENV: {os.environ.get('GOOGLE_VERTEXAI_LOCATION')}")
print(f"GOOGLE_CLOUD_PROJECT in ENV: {os.environ.get('GOOGLE_CLOUD_PROJECT')}")
print(f"GCLOUD_PROJECT in ENV: {os.environ.get('GCLOUD_PROJECT')}")
print(f"CLOUD_ML_PROJECT_ID in ENV: {os.environ.get('CLOUD_ML_PROJECT_ID')}")
print(f"GOOGLE_CLOUD_LOCATION in ENV: {os.environ.get('GOOGLE_CLOUD_LOCATION')}")
print(f"GOOGLE_CLOUD_REGION in ENV: {os.environ.get('GOOGLE_CLOUD_REGION')}")
print(f"CLOUD_ML_REGION in ENV: {os.environ.get('CLOUD_ML_REGION')}")
print(f"LOCATION in ENV: {os.environ.get('LOCATION')}")
print(f"GOOGLE_API_KEY in ENV: '{os.environ.get('GOOGLE_API_KEY')}'")
print("--------------------------------------\n")


# --- Agent Setup ---
# Initialize Agent WITHOUT project and location arguments.
# It should pick up the configuration from the environment variables set above
# AND potentially from the explicit vertexai.init() call.
print("Initializing Agent...")
try:
    # Use the simpler ADK model alias like "gemini-1.5-flash"
    simple_model_name = settings.DEFAULT_MODEL # Assuming settings.DEFAULT_MODEL is "gemini-1.5-flash" or similar
    print(f"Attempting to initialize Agent with ADK model alias: {simple_model_name}")

    agent = Agent(
        name="TravelPlanner",
        model=simple_model_name, # Use the simple alias here!
        instruction="You are an expert travel planner. For any user query, suggest the best time to visit, what to pack, "
        "and estimate expenses. Use tools as needed.",
        tools=[google_search],
        description="Helps users plan trips with smart suggestions."
        # NO 'project' or 'location' arguments here!
        # NO 'client' argument (ADK doesn't expose this for genai backend currently)
    )
    # Print the actual model name that the agent instance has (should be the alias)
    print(f"Agent initialized successfully using model: {agent.model}")
except Exception as e:
    print(f"ERROR initializing Agent: {e}")
    print("Check if the model name is correct and available in the specified Vertex project/location.")
    print("Also verify environment variables, ADC credentials, and vertexai.init() call.")
    traceback.print_exc() # Print traceback for initialization error
    raise # Re-raise the error to stop the application if agent fails

# --- Session and Runner Setup ---
print("Initializing Session Service...")
session_service = InMemorySessionService()
session_id = "travel_session"
try:
    # Attempt to create a new session. If it exists (e.g., during hot reload), catch the error.
    session_service.create_session(app_name="TravelPlanner", user_id="demo_user", session_id=session_id)
    print(f"Session '{session_id}' created.")
except Exception as e:
     # Check if the error indicates the session already exists
    # Note: The exact error string might vary by library version or database
    if "already exists" in str(e) or "UNIQUE constraint failed" in str(e):
         print(f"Session '{session_id}' likely already exists. Continuing.")
    else:
        print(f"An unexpected error occurred trying to create or access session '{session_id}': {e}")
        # Depending on severity, you might want to re-raise or handle differently
        # raise
    pass # Continue execution, assuming the session is usable

print("Initializing Runner...")
# The runner links the agent, session service, and handles execution flow
runner = Runner(agent=agent, app_name="TravelPlanner", session_service=session_service)
print("Runner initialized.")


# --- Agent Execution Function ---
# This function will be called by your API endpoint (e.g., FastAPI)
def run_travel_agent(prompt: str) -> str:
    print(f"\n--- Running travel agent for prompt: '{prompt}' ---")
    # The ADK runner expects a message object with a 'parts' attribute
    content = SimpleNamespace(role="user", parts=[SimpleNamespace(text=prompt)])
    final_response = None # Initialize to None
    full_response_text = "" # Accumulate intermediate text if needed

    try:
        # The runner.run() method handles the async invocation in a separate thread
        # It yields events as the agent processes the request.
        print(f"Invoking runner.run for session '{session_id}'...")
        events = runner.run(user_id="demo_user", session_id=session_id, new_message=content)

        print("Waiting for agent response events...")
        # Iterate through the events yielded by the runner
        for event in events:
            print(f"  Received event: type={event.type}") # Log the event type

            # A final response event contains the agent's completed answer
            if event.is_final_response():
                final_response = "".join(part.text for part in event.content.parts if hasattr(part, "text"))
                print(f"  >>> Final response received: '{final_response}'")
                # Don't return immediately, let the loop finish in case there are other events
                break # Exit loop once final response is found, assuming only one needed

            # Log other event types for debugging
            elif event.is_tool_code():
                # This event contains the code the agent decides to run (e.g., tool calls)
                 print(f"  Tool code generated: {event.content.parts}")
            elif event.is_tool_result():
                # This event contains the result from executing a tool
                 print(f"  Tool result received: {event.content.parts}")
            elif event.is_intermediate_response():
                 # An intermediate response provides partial text or updates during processing
                 intermediate_text = "".join(part.text for part in event.content.parts if hasattr(part, "text"))
                 print(f"  Intermediate response: '{intermediate_text}'")
                 # You might want to accumulate intermediate text if the final response
                 # doesn't always contain the full conversation turn, depending on agent behavior.
                 full_response_text += intermediate_text


        # After the loop finishes, check if a final response was captured
        if final_response is not None:
            print("--- Agent run finished successfully ---")
            return final_response
        elif full_response_text:
             # If no final response event but intermediate text was received, return that.
             # This can happen if the agent completes without explicitly yielding is_final_response().
             print("--- Agent run finished with intermediate text but no final response event ---")
             return full_response_text
        else:
            print("--- Agent run finished but NO response text was received ---")
            return "Error: No response received from Travel Agent."

    except Exception as e:
        # Catch any exception during the runner execution
        print(f"!!! ERROR during agent execution: {e} !!!")
        # Log the full traceback for detailed debugging
        traceback.print_exc()
        return f"Error during agent execution: {e}"

# Example usage (for testing if running script directly)
# if __name__ == "__main__":
#     # In a real application, this function would be called by your web framework endpoint
#     test_prompt = "What is the best time to visit Dubai?"
#     response = run_travel_agent(test_prompt)
#     print(f"\nTravel Agent Final Output:\n{response}")

#     test_prompt_2 = "Suggest some things to do there."
#     response_2 = run_travel_agent(test_prompt_2)
#     print(f"\nTravel Agent Final Output (follow-up):\n{response_2}")