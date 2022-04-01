from fastapi import APIRouter
from fastapi.params import Query
from fastapi_cache.decorator import cache

from app.schemas.math import FloatResult, IntResult
from app.core import operations

router = APIRouter()


@cache
@router.get("/pow", response_model=FloatResult)
async def power(base: float = Query(..., description="The base."),
                exp: float = Query(..., description="The exponent")):
    """The power of two numbers. (base ^ exp)"""
    return FloatResult(
        result=operations.power(base, exp)
    )


@cache
@router.get("/fibonacci", response_model=IntResult)
async def n_th_fibonacci(n: int = Query(..., ge=1)):
    """N-th Fibonacci number."""
    return IntResult(
        result=operations.n_th_fibonacci(n)
    )


@cache
@router.get("/factorial", response_model=IntResult)
async def factorial(n: int = Query(..., ge=1)):
    """n! Factorial"""
    return IntResult(
        result=operations.factorial(n)
    )
