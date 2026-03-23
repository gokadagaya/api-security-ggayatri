import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")


def get_weather(city):
    # Check if API key is available
    if not API_KEY:
        return "Error: API key not configured properly."

    url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(
            url,
            params={
                "q": city,
                "appid": API_KEY
            },
            timeout=5
        )

        # ✅ Handle rate limiting (Task 2)
        if response.status_code == 429:
            return "Too many requests. Please try again later."

        # Handle invalid API key
        if response.status_code == 401:
            return "Invalid API key. Please check your configuration."

        # Raise error for other bad responses
        response.raise_for_status()

        data = response.json()
        return data

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."

    except requests.exceptions.ConnectionError:
        return "Network error. Please check your internet connection."

    except requests.exceptions.RequestException as e:
        return f"Unexpected error occurred: {e}"


if __name__ == "__main__":
    city = "Hyderabad"

    # Removed logging for privacy (Task 3)
    # We should not log user location data as it is sensitive.
    # Logging city names may violate privacy principles like GDPR (data minimization).

    result = get_weather(city)
    print(result)
