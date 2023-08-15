from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import POSTGRES_URI

engine = create_engine(POSTGRES_URI, echo=True)

db_session = scoped_session(sessionmaker(autoflush=False, autocommit=False, bind=engine))
