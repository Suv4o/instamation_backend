from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base

from config.database import db_session

Model = declarative_base()
Model.query = db_session.query_property()


class TimeStampedModel(Model):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
