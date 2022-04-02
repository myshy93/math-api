import logging
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.api_v1.api import api_router
from app.core import config
from app.core.config import settings
from app.core.middlewares import store_requests_in_db
from app.core.security import create_access_token
from app.core.utils import init_logger
from app.db.connection import get_db, get_global_session, close_global_session
from app.db.init_db import init_db
from app.db.operations import authenticate_user
from app.schemas.users import Token

# Logger
init_logger()
logger = logging.getLogger(config.LOGGER_NAME)

# The app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Middlewares
# Limit request origin to a list of hosts.
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*" if settings.DEBUG else settings.SERVER_URL]
)
# Record any request in DB
app.add_middleware(BaseHTTPMiddleware, dispatch=store_requests_in_db)
# -----------

# Routers
app.include_router(api_router, prefix=settings.API_V1_STR)


# -----------


# On startup
@app.on_event("startup")
async def startup():
    # add caching - in memory
    FastAPICache.init(InMemoryBackend, prefix="fastapi-cache")
    logger.info("Cache opened.")
    # init database
    init_db()
    logger.info("Database initialized.")
    # open global db session used to store requests
    # it is useless and time-consuming to open a db session for each request.
    get_global_session()
    logger.info("Global db session opened.")


# -----------

# On shutdown
@app.on_event("shutdown")
async def shutdown():
    # close db session used to store requests
    close_global_session()
    logger.info("Global db session closed.")


# JWT token endpoint
@app.post("/token", response_model=Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)
# -----------
