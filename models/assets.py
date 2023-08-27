import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship

from models.base import TimeStampedModel


class Assets(TimeStampedModel):
    __tablename__ = "assets"

    aid = Column("id", String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    url = Column(String(1000), nullable=True)
    original_filename = Column(String(1000), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    user = Relationship("Users", back_populates="asset")

    def __repr__(self):
        return f"{self.__class__.__name__}, id: {self.aid}, url: {self.url}, original_filename: {self.original_filename}, stored_filename: {self.stored_filename}"
