from fastapi import APIRouter, HTTPException
from httpx import AsyncClient, Timeout, HTTPStatusError, RequestError

from app.config import settings
from app.schema.request import InferRequest
from app.utils.logging import AppLogger

router = APIRouter()
logger = AppLogger().get_logger()


@router.post("/chat")
async def generate(request: InferRequest):
    url = settings.OLLAMA_INFER_URL
    payload = request.model_dump()

    logger.info(f"Sending request to {url} with payload: {payload}")
    timeout = Timeout(30.0, connect=10.0)

    try:
        async with AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except HTTPStatusError as e:
        logger.error(f"HTTPStatusError: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except RequestError as e:
        logger.error(f"RequestError: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.debug(f"An unexpected error occurred: {str(e)}")
        logger.exception("An unexpected error occurred")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")