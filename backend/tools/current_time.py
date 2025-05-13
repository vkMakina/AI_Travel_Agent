

from datetime import datetime


def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """
    print(f"[DEBUG] Starting 'get_current_time'")
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }