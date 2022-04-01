from typing import Union

from sqlalchemy.orm import Session

from app.core.utils import get_hashed_password, verify_password
from app.models.user import UserModel
from app.schemas.users import UserCreateSchema, UserSchema


# + User operations
def create_user(db: Session, user: UserCreateSchema):
    hash_pass = get_hashed_password(user.password)
    db_user = UserModel(email=user.email, name=user.name, password=hash_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Union[None, UserSchema]:
    db_user = get_user_by_email(db, email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return UserSchema(email=db_user.email, name=db_user.name)

# - User operations
