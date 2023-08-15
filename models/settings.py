from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship
from models.base import TimeStampedModel


class Settings(TimeStampedModel):
    __tablename__ = "settings"

    sid = Column("id", Integer, primary_key=True, autoincrement=True)
    instagram_username = Column(String(30), nullable=True)
    instagram_password = Column(String(30), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)

    user = Relationship("Users", back_populates="setting")

    def __repr__(self):
        return f"{self.__class__.__name__}, id: {self.sid}, instagram_username: {self.instagram_username}, instagram_password: {self.instagram_password}"
