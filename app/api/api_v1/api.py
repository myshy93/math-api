from fastapi import APIRouter, Depends

from app.api.api_v1.endpoints import math
from app.core.security import oauth2_scheme

api_router = APIRouter(dependencies=[Depends(oauth2_scheme)])
api_router.include_router(math.router, tags=["Operations"], prefix="/math")
