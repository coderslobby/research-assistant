from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class ConfigSettings(BaseSettings):
    COHERE_API_KEY: str
    GROW_API_KEY: str
    PINECONE_API_KEY: str
    LLM_MODEL: str
    TAVILY_API_KEY:str

    APP_NAME: str
    APP_ENV: str
    APP_PORT: int

    TOPIC_MIN_LEN: int
    TOPIC_MAX_LEN: int

    MIN_RESULTS: int
    MAX_RESULTS: int

    MAX_TOKENS: int
    TEMPRATURE: float

    LOG_LEVEL: str = "Debug"

    SUPABASE_URL: str
    SUPABASE_KEY: str
    SENTRY_DSN: str

    verify_api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = ConfigSettings()
        