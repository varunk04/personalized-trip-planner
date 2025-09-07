from fastapi import FastAPI
from app.config import settings
from app.routes.itinerary import router as itinerary_router

app = FastAPI(
    title="Personalized Trip Planner AI",
    description="AI-powered trip planner with real-time data aggregation",
    version="1.0.0"
)

app.include_router(itinerary_router, prefix="/api/v1", tags=["Itinerary"])

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "geoapify_key_loaded": bool(settings.GEOAPIFY_API_KEY),
        "weather_service": "open-meteo (no key required)"
    }
