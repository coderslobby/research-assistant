from groq import AsyncGroq
from app.core.logger import logger
from app.core.config import settings
from app.core.exceptions import LLMException
from typing import  Optional

class LLMClient():
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROW_API_KEY)
        self.model = settings.LLM_MODEL
    
    async def generate(self, question: str, system_prompt: Optional[str] = None) -> str:
        messages = []

        if system_prompt:
            messages.append({
                'role':'system',
                'content':system_prompt
            })
        messages.append({
            'role':'user',
            'content':question
            })
        try:
            logger.debug(f"Calling LLM with prompt length: {len(question)}")
            response = await self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPRATURE
            )

            result = response.choices[0].message.content
            logger.debug(f"LLM response received, length: {len(result)}")
            return result
        except Exception as e:
            logger.error(f'LLM call failed: {str(e)}')
            raise LLMException(f'LLM call failed: {str(e)}')
        
llm_client = LLMClient()