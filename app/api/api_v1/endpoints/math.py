from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from starlette import status

from app.core import operations
from app.core.event_producer import send_math_event
from app.core.security import get_current_user
from app.schemas.math import FloatResult, IntResult
from app.schemas.users import UserSchema

router = APIRouter()

extra_responses = {
    409: {"description": "Requested operation is requires to much resources."}
}


@router.get("/pow", response_model=FloatResult, responses=extra_responses)
async def power(base: float = Query(..., description="The base."),
                exp: float = Query(..., description="The exponent")):
    """The power of two numbers. (base ^ exp)"""
    await send_math_event("power called")
    try:
        res = operations.power(base, exp)
    except OverflowError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Result exceeds memory limits.",
        )
    return FloatResult(
        result=res
    )


@router.get("/fibonacci", response_model=IntResult)
async def n_th_fibonacci(n: int = Query(..., ge=1)):
    """N-th Fibonacci number."""
    await send_math_event("fibonacci called")
    return IntResult(
        result=operations.n_th_fibonacci(n)
    )


# noinspection PyUnusedLocal
@router.get("/factorial", response_model=IntResult)
async def factorial(n: int = Query(..., ge=1),
                    c_user: UserSchema = Depends(get_current_user)):
    """n! Factorial"""
    await send_math_event("factorial called")
    return IntResult(
        result=operations.factorial(n)
    )
