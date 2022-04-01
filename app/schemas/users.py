from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    """Base user model."""
    email: str
    name: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserSchema):
    """User model for user creation."""
    password: str


class TokenData(BaseModel):
    """Token extracted data."""
    username: Optional[str] = None


class Token(BaseModel):
    """New token request response."""
    access_token: str
    token_type: str = "bearer"
