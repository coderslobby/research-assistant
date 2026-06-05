from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

class ResearchResponse(BaseModel):
    topic: str
    answer: str
    sources: List[str]
    status: str
    timestamp: datetime = datetime.now(timezone.utc)

class ErrorResponse(BaseModel):
    status_code: str = 'error'
    message: str
    details: Optional[str]