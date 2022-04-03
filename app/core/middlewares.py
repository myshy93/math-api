from starlette.requests import Request

from app.db.connection import get_global_session
from app.db.operations import add_request_record


async def store_requests_in_db(request: Request, call_next):
    db = get_global_session()
    add_request_record(db, request)
    return await call_next(request)