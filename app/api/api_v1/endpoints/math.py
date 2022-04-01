from fastapi import APIRouter
from fastapi.params import Query

from app.schemas.math import FloatResult, IntResult
from app.core import operations

router = APIRouter()


@router.get("/pow", response_model=FloatResult)
def power(base: float = Query(..., description="The base."),
          exp: float = Query(..., description="The exponent")):
    """The power of two numbers. (base ^ exp)"""
    return FloatResult(
        result=operations.power(base, exp)
    )


@router.get("/fibonacci", response_model=IntResult)
def n_th_fibonacci(n: int):
    """N-th Fibonacci number."""
    return IntResult(
        result=operations.n_th_fibonacci(n)
    )


@router.get("/factorial", response_model=IntResult)
def factorial(n: int):
    """n! Factorial"""
    return IntResult(
        result=operations.factorial(n)
    )
