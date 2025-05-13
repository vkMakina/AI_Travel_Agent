# backend/services/utils.py – Reusable Helpers

def clean_text_response(text: str) -> str:
    """Clean up Gemini responses (remove double newlines, extra spaces, etc)."""
    cleaned = text.strip().replace('\n\n', '\n').replace('  ', ' ')
    return cleaned
