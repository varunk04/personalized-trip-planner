from fastapi import APIRouter, HTTPException
import asyncio
import time
from app.schemas import ItineraryContextRequest, ItineraryContextResponse, PlaceInfo, WeatherInfo
from app.services.places import GeoapifyPlacesClient
from app.services.weather import OpenMeteoClient  # Updated import

router = APIRouter()

@router.post("/itinerary/context", response_model=ItineraryContextResponse)
async def get_itinerary_context(request: ItineraryContextRequest):
    """Fetch places and weather data for LLM to generate itinerary"""
    
    start_time = time.time()
    location = (request.lat, request.lng)
    radius_m = request.radius_km * 1000
    
    # Initialize clients
    places_client = GeoapifyPlacesClient()
    weather_client = OpenMeteoClient()  # No API key needed!
    
    try:
        # Concurrent API calls
        places_task = places_client.nearby_search(location, radius_m)
        weather_task = weather_client.get_current_weather(location)
        
        places_data, weather_data = await asyncio.gather(places_task, weather_task)
        
        # Normalize places data
        normalized_places = places_client.normalize_place_data(places_data)
        
        # Extract top attractions
        attractions = []
        for place in normalized_places['results'][:request.max_results]:
            attractions.append(PlaceInfo(
                name=place['name'],
                vicinity=place['vicinity'],
                location=place['location'],
                categories=place['categories'],
                rating=place['rating']
            ))
        
        # Normalize weather data
        weather_info = WeatherInfo(
            description=weather_data['weather'][0]['description'],
            temperature=weather_data['main']['temp'],
            feels_like=weather_data['main']['feels_like'],
            humidity=weather_data['main']['humidity']
        )
        
        # Response metadata
        meta = {
            "provider": "geoapify_openmeteo",
            "request_time_ms": round((time.time() - start_time) * 1000),
            "places_count": len(attractions),
            "search_radius_km": request.radius_km
        }
        
        return ItineraryContextResponse(
            attractions=attractions,
            weather=weather_info,
            meta=meta
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch context: {str(e)}")
