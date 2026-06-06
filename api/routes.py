from fastapi import APIRouter, status, HTTPException, Request, Depends
from app.core.logger import logger
from app.core.exceptions import ResearchException
from models.request import ResearchRequest
from models.response import ResearchResponse, ErrorResponse
from services.research_services import research_services
from app.security.security import verify_api_key
from app.core.limiter import limiter

router = APIRouter(
    prefix='/research',
    tags=['research']
)

@router.post(
    "/",
    response_model=ResearchResponse,
    status_code=status.HTTP_200_OK,
    responses={
        500: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    }
)
@limiter.limit("5/minute")
async def research(request: Request ,body: ResearchRequest, api_key: str = Depends(verify_api_key)):
    logger.info(f"Recieved the topic {body.topic} for research")
    try:
        result = await research_services.research(body)
        return result
    except ResearchException as e:
        logger.error(f"Exception occured for the topic {body.topic} | {e.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )