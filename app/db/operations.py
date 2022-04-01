from sqlalchemy.orm import Session

from app.core.security import get_hashed_password
from app.models.user import UserModel
from app.schemas.users import UserCreateSchema


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

# - User operations
