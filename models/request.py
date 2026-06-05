from pydantic import BaseModel, field_validator
from app.core.config import settings

class ResearchRequest(BaseModel):
    topic: str
    max_result: int = settings.MAX_RESULTS

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value:str):
        if not value.strip():
            raise ValueError("topic cannot be empty or whitespace")
        if len(value) < settings.TOPIC_MIN_LEN:
            raise ValueError(f"topic must be at least {settings.TOPIC_MIN_LEN} characters")
        if len(value) > settings.TOPIC_MAX_LEN:
            raise ValueError(f"topic cannot exceed {settings.TOPIC_MAX_LEN} characters")
        return value.strip()
    
    @field_validator("max_result")
    @classmethod
    def max_result_validate(cls, value:int):
        if value < settings.MIN_RESULTS:
            raise ValueError(f"max_results must be at least {settings.MIN_RESULTS}")
        if value > settings.MAX_RESULTS:
            raise ValueError(f"max_results cannot exceed {settings.MAX_RESULTS}")
        return value