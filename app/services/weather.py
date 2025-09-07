import httpx
import backoff
from typing import Tuple, Dict, Any, Optional
from app.config import settings

class OpenMeteoClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self):
        # No API key needed!
        pass

    @backoff.on_exception(backoff.expo, httpx.HTTPStatusError, max_tries=3)
    async def get_current_weather(self, location: Tuple[float, float]) -> Optional[Dict[str, Any]]:
        """Get current weather from Open-Meteo (completely free, no API key)"""
        lat, lng = location
        
        params = {
            "latitude": lat,
            "longitude": lng,
            "current_weather": True,
            "temperature_unit": "celsius",
            "windspeed_unit": "kmh"
        }
        
        timeout = httpx.Timeout(settings.HTTP_TIMEOUT_SECONDS)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            current = data.get('current_weather', {})
            if not current:
                raise ValueError('No current weather data returned')
            
            # Normalize to match expected format
            return {
                'weather': [{'description': self._get_weather_description(current.get('weathercode', 0))}],
                'main': {
                    'temp': current.get('temperature'),
                    'feels_like': current.get('temperature'),  # Open-Meteo doesn't provide feels_like
                    'humidity': 50  # Default since not provided in current_weather
                },
                'wind': {
                    'speed': current.get('windspeed'),
                    'deg': current.get('winddirection')
                },
                'dt': current.get('time')
            }
    
    def _get_weather_description(self, weather_code: int) -> str:
        """Convert Open-Meteo weather code to description"""
        weather_descriptions = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            56: "Light freezing drizzle", 57: "Dense freezing drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            66: "Light freezing rain", 67: "Heavy freezing rain",
            71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }
        return weather_descriptions.get(weather_code, f"Unknown weather code: {weather_code}")
