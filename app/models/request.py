from sqlalchemy import Column, Integer, String, ForeignKey, Float

from app.db.base_class import Base


class RequestModel(Base):
    # noinspection SpellCheckingInspection
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String)
    ts = Column(Float)
    ip = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
