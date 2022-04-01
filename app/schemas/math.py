import numbers

from pydantic import BaseModel, Field


class FloatResult(BaseModel):
    """Simple float math result."""
    result: float = Field(
        description="Operation result"
    )


class IntResult(BaseModel):
    """Simple integer math result."""
    result: int = Field(
        description="Operation result"
    )
