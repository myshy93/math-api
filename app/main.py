from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.core.config import settings
from app.api.api_v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():
    # add caching - in memory
    FastAPICache.init(InMemoryBackend, prefix="fastapi-cache")
