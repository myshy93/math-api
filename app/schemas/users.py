from pydantic import BaseModel


class UserSchema(BaseModel):
    """Base user model."""
    email: str
    name: str


class UserCreateSchema(UserSchema):
    """User model for user creation."""
    password: str
