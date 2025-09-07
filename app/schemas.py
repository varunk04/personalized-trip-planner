from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ItineraryContextRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude") 
    radius_km: int = Field(default=5, ge=1, le=30, description="Search radius in km")
    max_results: int = Field(default=12, ge=1, le=20, description="Max places to return")

class WeatherInfo(BaseModel):
    description: str
    temperature: float
    feels_like: float
    humidity: int

class PlaceInfo(BaseModel):
    name: str
    vicinity: str
    location: Dict[str, float]
    categories: List[str]
    rating: Optional[float] = None

class ItineraryContextResponse(BaseModel):
    attractions: List[PlaceInfo]
    weather: WeatherInfo
    meta: Dict[str, Any]
