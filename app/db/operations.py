from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import UserModel
from app.schemas.users import UserCreateSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# + User operations
def create_user(db: Session, user: UserCreateSchema):
    hash_pass = pwd_context.hash(user.password)
    db_user = UserModel(email=user.email, name=user.name, password=hash_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


# - User operations
