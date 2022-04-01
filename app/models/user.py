from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class UserModel(Base):
    # noinspection SpellCheckingInspection
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
