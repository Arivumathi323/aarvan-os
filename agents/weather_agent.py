import requests

# Using Open-Meteo — 100% free, no API key needed da!
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Weather code descriptions
WEATHER_CODES = {
    0: "☀️ Clear sky",
    1: "🌤️ Mainly clear",
    2: "⛅ Partly cloudy",
    3: "☁️ Overcast",
    45: "🌫️ Foggy",
    48: "🌫️ Icy fog",
    51: "🌦️ Light drizzle",
    61: "🌧️ Slight rain",
    63: "🌧️ Moderate rain",
    65: "🌧️ Heavy rain",
    71: "🌨️ Slight snow",
    80: "🌦️ Rain showers",
    95: "⛈️ Thunderstorm",
}

class WeatherAgent:
    def execute(self, action: str, params: dict) -> str:
        city = (
            params.get("city", "") or
            params.get("location", "") or
            params.get("place", "Chennai")   # Default to Chennai da
        )
        return self.get_weather(city)

    def get_weather(self, city: str = "Chennai") -> str:
        try:
            # Step 1 — Get coordinates
            geo = requests.get(
                GEOCODE_URL,
                params={"name": city, "count": 1, "language": "en"},
                timeout=5
            ).json()

            if not geo.get("results"):
                return f"❌ City '{city}' not found da"

            loc = geo["results"][0]
            lat = loc["latitude"]
            lon = loc["longitude"]
            name = loc["name"]
            country = loc.get("country", "")

            # Step 2 — Get weather
            weather = requests.get(
                WEATHER_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "wind_speed_10m",
                        "weather_code"
                    ],
                    "timezone": "auto"
                },
                timeout=5
            ).json()

            current = weather["current"]
            temp = current["temperature_2m"]
            humidity = current["relative_humidity_2m"]
            wind = current["wind_speed_10m"]
            code = current["weather_code"]
            condition = WEATHER_CODES.get(code, "🌡️ Unknown")

            return (
                f"🌍 Weather in {name}, {country}:\n"
                f"  {condition}\n"
                f"  🌡️  Temperature: {temp}°C\n"
                f"  💧 Humidity: {humidity}%\n"
                f"  💨 Wind: {wind} km/h"
            )

        except requests.exceptions.ConnectionError:
            return "❌ No internet connection da — weather needs internet"
        except Exception as e:
            return f"❌ Weather error: {str(e)}"