from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Relationship
from models.base import TimeStampedModel


class Users(TimeStampedModel):
    __tablename__ = "users"

    uid = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column(String(320), nullable=False, unique=True)

    setting = Relationship("Settings", back_populates="user", uselist=False, passive_deletes=True)

    def __repr__(self):
        return f"{self.__class__.__name__}, id: {self.uid}, email: {self.email}"
