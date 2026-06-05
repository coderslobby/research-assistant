from fastapi import APIRouter, status, HTTPException
from loguru import logger
from app.core.exceptions import ResearchException
from models.request import ResearchRequest
from models.response import ResearchResponse, ErrorResponse
from services.research_services import research_services

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

async def research(request: ResearchRequest):
    logger.info(f"Recieved the topic {request.topic} for research")
    try:
        result = await research_services.research(request)
        return result
    except ResearchException as e:
        logger.error(f"Exception occured for the topic {request.topic} | {e.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )