from app.core.logger import logger
from app.core.exceptions import ResearchException, LLMException, DatabaseException
from app.core.config import settings
from tavily import TavilyClient
from models.request import ResearchRequest
from models.response import ResearchResponse
from repositories.research_repository import research_repository
from typing import Dict, List
from integrations.llm_client import llm_client
from typing import cast, Optional, Any
from datetime import datetime, timezone
import asyncio

class ResearchService():
    def __init__(self):
        self.tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)

    async def research(self, request:ResearchRequest) -> Optional[ResearchResponse]:
        try:
            cached = await research_repository.get_research(request.topic)
            if cached:
                logger.info(f"Returning cached research for topic: {request.topic}")
                return ResearchResponse(
                    topic=cast(str, cached['topic']),
                    answer=cast(str, cached['answer']),
                    sources=cast(List[str], cached['sources']),
                    status='success',
                    timestamp=cast(datetime,cached['created_at'])               
                )
            # web search
            logger.info(f"Searching web for topic: {request.topic}")
            search_result = await self._search_web(request.topic, request.max_result)

            #generate answer
            logger.info(f"Generating answer for topic: {request.topic}")
            answer = await self._generate_answer(request.topic, search_result)

            # save answer to DB
            await research_repository.save_research(
                topic=request.topic,
                answer=answer,
                sources=cast(List[str], search_result['sources'])
            )
            return ResearchResponse(
                topic=request.topic,
                answer=answer,
                sources=search_result['sources'],
                status='success',
                timestamp=datetime.now(timezone.utc)
            )
        except LLMException as e:
            logger.error(f"LLM failed during research: {e.message}")
            raise LLMException(f"Research failed: {e.message}")
        except DatabaseException as e:
            logger.error(f"Database failed during research: {e.message}")
            raise DatabaseException(f"Research failed: {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error during research: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")


    async def _search_web(self, topic: str, max_result: int) -> Dict[str, Any]:
        try:
            results = cast(
                Dict[str, Any], await asyncio.to_thread(
                self.tavily.search,
                query=topic,
                max_results=max_result
            ))
            content = "\n\n".join([r["content"] for r in results["results"]])
            sources: List[str] = [r["url"] for r in results["results"]]

            return {'content':content,'sources':sources}
        except Exception as e:
            logger.error(f"Web search failed: {str(e)}")
            raise ResearchException(f"Web search failed: {str(e)}")
    
    async def _generate_answer(self, topic: str, search_content: Dict[str, str | List[str]]) -> str:
        system_prompt = """You are a research assistant. 
        Given a topic and search results, provide a clear, 
        accurate and concise research summary.
        Always base your answer strictly on the provided search results."""

        prompt = f"""
        Topic: {topic}

        Search Results:
        {search_content}

        Provide a comprehensive research summary based on the above results.
        """
        return await llm_client.generate(
            question=topic,
            system_prompt=system_prompt
        )
    
research_services = ResearchService()