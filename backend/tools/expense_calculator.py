import os
from typing import Optional
import requests
from google.generativeai import GenerativeModel
from config import settings

SERP_API_KEY = settings.SERPAPI_API_KEY #os.getenv("SERPAPI_API_KEY")
model = settings.DEFAULT_MODEL #GenerativeModel(model_name="gemini-2.0-flash-lite")

def get_estimated_expense(destination: str) -> dict:
    """Estimates travel expenses using SerpAPI. Returns daily or total cost based on number of days."""
    
    print(f"[DEBUG] Starting 'get_estimated_expense'")
    print(f"[DEBUG] Destination received: {destination}")

    try:
        query = f"Average travel cost in {destination} per day"
        print(f"[DEBUG] Formulated SerpAPI query: {query}")

        serp_api_url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": SERP_API_KEY,
            "engine": "google",
            "num": 5
        }

        print(f"[DEBUG] Sending request to SerpAPI with params: {params}")
        response = requests.get(serp_api_url, params=params)
        data = response.json()

        snippets = [
            r["snippet"] for r in data.get("organic_results", []) if "snippet" in r
        ]

        print(f"[DEBUG] Extracted snippets from SerpAPI response:")
        for s in snippets:
            print(f"   - {s}")

        # Try extracting cost
        daily_cost = None
        for snippet in snippets:
            if "$" in snippet or "USD" in snippet:
                try:
                    tokens = snippet.replace(",", "").split()
                    for i, token in enumerate(tokens):
                        if "$" in token or "USD" in token:
                            num = ''.join([c for c in token if c.isdigit()])
                            if num:
                                daily_cost = int(num)
                                print(f"[DEBUG] Extracted daily cost from snippet: ${daily_cost}")
                                break
                    if daily_cost:
                        break
                except Exception as parse_err:
                    print(f"[WARNING] Failed to parse snippet: {parse_err}")
                    continue

        # Fallback to LLM if cost not found
        if not daily_cost:
            print("[DEBUG] Could not extract cost from snippets. Falling back to LLM.")
            prompt = f"What is the average daily cost in {destination} in USD for a tourist?"
            print(f"[DEBUG] LLM prompt: {prompt}")
            llm_response = model.generate_content(prompt)
            print(f"[DEBUG] LLM response: {llm_response.text}")
            daily_cost = _extract_cost_from_text(llm_response.text)
            print(f"[DEBUG] Cost extracted from LLM: ${daily_cost if daily_cost else 'None'}")

        if not daily_cost:
            print("[ERROR] Unable to determine daily cost from both SerpAPI and LLM.")
            return {"status": "error", "message": f"Could not determine travel cost for {destination}."}

        
        print(f"[DEBUG] Returning daily cost: ${daily_cost}")
        return {
            "status": "success",
            "destination": destination,
            "daily_cost": daily_cost,
            "message": f"The average daily cost in {destination} is approximately ${daily_cost}."
        }

    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")
        return {"status": "error", "message": str(e)}


def _extract_cost_from_text(text: str) -> int:
    """Helper function to extract cost from LLM response text."""
    import re
    matches = re.findall(r"\$?(\d{2,5})", text.replace(",", ""))
    if matches:
        print(f"[DEBUG] Regex matched numbers in LLM response: {matches}")
        return int(matches[0])
    print("[DEBUG] No matches found in LLM response.")
    return None
