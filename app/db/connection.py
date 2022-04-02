from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)
# Session manager
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

_global_session = None


def get_global_session():
    global _global_session
    if not isinstance(_global_session, Session):
        _global_session = SessionLocal()
    return _global_session


def close_global_session():
    if isinstance(_global_session, Session):
        _global_session.close()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
