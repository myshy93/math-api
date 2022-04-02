import logging

from sqlalchemy.exc import IntegrityError

from app.core import config
from app.core.config import settings, default_user
from app.db.base_class import Base
from app.db.connection import engine, SessionLocal
from app.db.operations import create_user
from app.schemas.users import UserCreateSchema

# Logger
logger = logging.getLogger(config.LOGGER_NAME)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    if settings.DEBUG:
        db = SessionLocal()
        user = UserCreateSchema(
            email=default_user["email"],
            password=default_user["password"],
            name=default_user["name"]
        )
        try:
            create_user(db, user)
        except IntegrityError:
            logger.warning("Test user already in database.")
        db.close()
