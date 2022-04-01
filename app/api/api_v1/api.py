from fastapi import APIRouter

from app.api.api_v1.endpoints import math

api_router = APIRouter()
api_router.include_router(math.router, tags=["Operations"], prefix="/math")
