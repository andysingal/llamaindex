from fastapi import APIRouter

from app.api.endpoints import endpoint_ping, endpoint_infer, endpoint_search

api_router = APIRouter()

api_router.include_router(endpoint_ping.router, tags=["ping"])
api_router.include_router(endpoint_infer.router, prefix="/infer", tags=["infer"])
api_router.include_router(endpoint_search.router, prefix="/search", tags=["search"])