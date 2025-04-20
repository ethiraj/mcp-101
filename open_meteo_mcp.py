# /// script
# dependencies = ["fastmcp", "httpx"]
# ///
# Example usage:
# uv pip install fastmcp httpx
# fastmcp run open_meteo_mcp.py
# Or: python open_meteo_mcp.py

import httpx
from pydantic import BaseModel, Field

from fastmcp import FastMCP


# Define the response structure for clarity and potential validation
class WeatherResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    temperature: float = Field(alias="current_temperature")
    temperature_unit: str
    weather_description: str
    wind_speed: float = Field(alias="current_wind_speed")
    wind_speed_unit: str
    error: str | None = None  # Include an error field


# Helper function to map WMO weather codes to descriptions
# Source: https://open-meteo.com/en/docs#weathervariables
def get_weather_description(code: int) -> str:
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return descriptions.get(code, f"Unknown code ({code})")


# Create the FastMCP Server instance
# Add httpx as a dependency for when installed via `fastmcp install`
mcp = FastMCP("Open-Meteo Weather", dependencies=["httpx"])


@mcp.tool()
async def get_current_weather(location: str) -> WeatherResponse | dict[str, str]:
    """
    Gets the current weather for a specified location.
    It first finds the latitude and longitude for the location,
    then fetches the current weather conditions.
    """
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    forecast_url = "https://api.open-meteo.com/v1/forecast"
    # Use Fahrenheit for broader US audience compatibility, easily changed
    temp_unit = "fahrenheit"

    async with httpx.AsyncClient() as client:
        # 1. Geocode the location to get latitude and longitude
        try:
            geocode_params = {
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json",
            }
            response = await client.get(
                geocode_url, params=geocode_params, timeout=10.0
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            geocode_data = response.json()

            if not geocode_data.get("results"):
                return {"error": f"Could not find location: {location}"}

            geo_result = geocode_data["results"][0]
            latitude = geo_result["latitude"]
            longitude = geo_result["longitude"]
            found_location_name = geo_result.get(
                "name", location
            )  # Use found name if available

        except httpx.HTTPStatusError as e:
            return {
                "error": f"Geocoding API error: {e.response.status_code} - {e.response.text}"
            }
        except (httpx.RequestError, Exception) as e:
            return {"error": f"Failed to connect to Geocoding API: {str(e)}"}

        # 2. Get the current weather using latitude and longitude
        try:
            forecast_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
                "temperature_unit": temp_unit,
                "wind_speed_unit": "mph",
                "timezone": "auto",  # Use auto timezone detection
            }
            response = await client.get(
                forecast_url, params=forecast_params, timeout=10.0
            )
            response.raise_for_status()
            weather_data = response.json()

            if "current_weather" not in weather_data:
                return {"error": "Could not retrieve current weather data."}

            current = weather_data["current_weather"]
            units = weather_data.get("current_weather_units", {})

            # Map weather code to description
            weather_description = get_weather_description(
                current.get("weathercode", -1)
            )

            # Prepare the successful response using the Pydantic model
            # Note the alias mapping for temperature and wind_speed
            weather_info = WeatherResponse(
                location=found_location_name,
                latitude=latitude,
                longitude=longitude,
                current_temperature=current.get("temperature", float("nan")),
                temperature_unit=units.get("temperature", temp_unit),
                weather_description=weather_description,
                current_wind_speed=current.get("windspeed", float("nan")),
                wind_speed_unit=units.get("windspeed", "mph"),
            )
            return weather_info

        except httpx.HTTPStatusError as e:
            return {
                "error": f"Weather API error: {e.response.status_code} - {e.response.text}"
            }
        except (httpx.RequestError, Exception) as e:
            return {"error": f"Failed to connect to Weather API: {str(e)}"}


if __name__ == "__main__":
    # This allows running the server directly using `python open_meteo_mcp.py`
    mcp.run()
