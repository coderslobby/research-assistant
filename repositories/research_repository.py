import httpx
from app.core.config import settings
from app.core.exceptions import DatabaseException
from loguru import logger
from typing import List, Optional

from models import response

class ResearchRepository():
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    async def save_research(self, topic: str, answer: str, sources: List[str]):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.url}/rest/v1/research_history",
                    headers=self.headers,
                    json={
                        "topic": topic,
                        "answer": answer,
                        "sources": sources
                    }
                )
                print(response.status_code)
                print(response.text)
                logger.debug(f"Research saved for topic: {topic}")
        except Exception as e:
            logger.error(f"Failed to save research: {str(e)}")
            raise DatabaseException(f"Failed to save research: {str(e)}")
        
    async def get_research(self, topic: str) -> Optional[dict]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.url}/rest/v1/research_history?select=topic,answer,sources,created_at&topic=eq.{topic}",
                    headers=self.headers
                )
                if response.status_code == 200:
                    data = response.json()
                    return data[0] if data else None
                else:
                    logger.error(f"Failed to fetch research data: {response.status_code}")
                    raise DatabaseException(f"Failed to fetch research data: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to fetch research data: {str(e)}")
            raise DatabaseException(f"Failed to fetch research data: {str(e)}")

research_repository = ResearchRepository()