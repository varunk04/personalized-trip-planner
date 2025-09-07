from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    GEOAPIFY_API_KEY: str = Field(..., env='GEOAPIFY_API_KEY')
    OPEN_WEATHER_API_KEY: str = Field(..., env='OPEN_WEATHER_API_KEY')
    HTTP_TIMEOUT_SECONDS: int = Field(default=6, env='HTTP_TIMEOUT_SECONDS')
    HTTP_MAX_RETRIES: int = Field(default=2, env='HTTP_MAX_RETRIES')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
