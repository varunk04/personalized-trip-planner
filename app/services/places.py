import httpx
import backoff
from typing import Tuple, Dict, Any, Optional
from app.config import settings

class GeoapifyPlacesClient:
    BASE_URL = "https://api.geoapify.com/v2/places"

    def __init__(self):
        self.api_key = settings.GEOAPIFY_API_KEY

    @backoff.on_exception(backoff.expo, httpx.HTTPStatusError, max_tries=3)
    async def nearby_search(self, location: Tuple[float, float], 
                           radius: int = 5000) -> Optional[Dict[str, Any]]:
        """Search for nearby attractions and restaurants"""
        lat, lng = location
        
        params = {
            "categories": "tourism.attraction,catering.restaurant",
            "filter": f"circle:{lng},{lat},{radius}",
            "limit": 20,
            "apiKey": self.api_key
        }
        
        timeout = httpx.Timeout(settings.HTTP_TIMEOUT_SECONDS)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()

    def normalize_place_data(self, geoapify_response: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Geoapify response to normalized format"""
        places = []
        
        for feature in geoapify_response.get('features', []):
            props = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            coords = geometry.get('coordinates', [0, 0])
            
            place = {
                'name': props.get('name', 'Unknown'),
                'vicinity': props.get('address_line2', ''),
                'location': {'lat': coords[1], 'lng': coords[0]},
                'place_id': props.get('place_id'),
                'categories': props.get('categories', []),
                'rating': props.get('rating'),
                'user_ratings_total': props.get('rating_count')
            }
            places.append(place)
        
        return {'results': places, 'status': 'OK'}
