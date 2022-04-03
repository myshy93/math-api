import logging
from datetime import timedelta

import sentry_sdk
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from kafka.errors import KafkaConnectionError
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.api_v1.api import api_router
from app.core import config, event_producer
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

# Init sentry
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # To set a uniform sample rate
    traces_sample_rate=1,
)

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
    logger.info("Cache opened.")
    # init database
    init_db()
    logger.info("Database initialized.")
    # open global db session used to store requests
    # it is useless and time-consuming to open a db session for each request.
    get_global_session()
    logger.info("Global db session opened.")
    try:
        logger.info("Connecting to Kafka broker....")
        await event_producer.start()
        logger.info("Connected to Kafka broker.")
    except KafkaConnectionError:
        logger.warning("Unable to connect to Kafka broker.")


# -----------

# On shutdown
@app.on_event("shutdown")
async def shutdown():
    # close db session used to store requests
    close_global_session()
    logger.info("Global db session closed.")
    await event_producer.stop()
    logger.info("Kafka broker connection closed closed.")


# JWT token endpoint
@app.post("/token", response_model=Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.debug(f"Auth failed for {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logger.debug(f"New token emitted to {user.email}")
    return Token(access_token=access_token)


# -----------

app = SentryAsgiMiddleware(app)
