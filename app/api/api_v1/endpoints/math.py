from fastapi import APIRouter, Depends
from fastapi.params import Query
from fastapi_cache.decorator import cache

from app.core.event_producer import producer
from app.core.security import get_current_user
from app.schemas.math import FloatResult, IntResult
from app.core import operations
from app.schemas.users import UserSchema

router = APIRouter()

KAFKA_MATH_TOPIC = 'math'


@cache
@router.get("/pow", response_model=FloatResult)
async def power(base: float = Query(..., description="The base."),
                exp: float = Query(..., description="The exponent")):
    """The power of two numbers. (base ^ exp)"""
    producer.send(KAFKA_MATH_TOPIC, b"power called")
    return FloatResult(
        result=operations.power(base, exp)
    )


@cache
@router.get("/fibonacci", response_model=IntResult)
async def n_th_fibonacci(n: int = Query(..., ge=1)):
    """N-th Fibonacci number."""
    producer.send(KAFKA_MATH_TOPIC, b"fibonacci called")
    return IntResult(
        result=operations.n_th_fibonacci(n)
    )


@cache
@router.get("/factorial", response_model=IntResult)
async def factorial(n: int = Query(..., ge=1),
                    c_user: UserSchema = Depends(get_current_user)):
    """n! Factorial"""
    producer.send(KAFKA_MATH_TOPIC, b"factorial called")
    return IntResult(
        result=operations.factorial(n)
    )
