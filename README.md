# Personalized Trip Planner

A FastAPI-based backend service for generating personalized travel itineraries using Google Places and OpenWeather APIs. Includes health checks, caching, rate limiting, and structured logging.

## Features

- **FastAPI**: High-performance API framework
- **Google Places**: Fetches location data for trip planning
- **OpenWeather**: Integrates weather data for destinations
- **Redis/In-memory Cache**: Caching layer for performance
- **Rate Limiting**: Token bucket per provider
- **Structured Logging**: Centralized logging configuration
- **Health Checks**: `/health` and `/ready` endpoints

## Project Structure

```
├── app/
│   ├── main.py                # FastAPI app, lifespan, routes include
│   ├── config.py              # Settings (Pydantic BaseSettings) + validation
│   ├── schemas.py             # Pydantic request/response models
│   ├── services/
│   │   ├── http.py            # shared httpx.AsyncClient with retry/backoff
│   │   ├── places.py          # Google Places client (server-side)
│   │   └── weather.py         # OpenWeather client
│   ├── routes/
│   │   ├── health.py          # GET /health, /ready
│   │   └── itinerary.py       # POST /itinerary/context
│   └── utils/
│       ├── cache.py           # simple Redis caching layer (optional fallback: in-memory)
│       ├── ratelimit.py       # token bucket per-provider
│       └── logger.py          # struct logging configuration
├── tests/
│   ├── test_health.py
│   ├── test_itinerary_context.py
│   └── conftest.py
├── pyproject.toml
├── .env.example
├── Dockerfile
└── README.md
```

## Setup

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd personalized-trip-planner
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in your API keys and settings.

4. **Run the application**
   ```sh
   uvicorn app.main:app --reload
   ```

5. **Run tests**
   ```sh
   pytest
   ```

## API Endpoints

- `GET /health` — Health check
- `GET /ready` — Readiness check
- `POST /itinerary/context` — Generate itinerary based on context

## Environment Variables

See `.env` for required variables (Google Places API key, OpenWeather API key, Redis URL, etc).

## Docker

To build and run with Docker:

```sh
docker build -t trip-planner .
docker run --env-file .env -p 8000:8000 trip-planner
```

## License

MIT

## Author
Varun Kumar Foujdhar