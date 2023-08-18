from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config.environments import POSTGRES_URI

engine = create_engine(POSTGRES_URI, echo=False)

db_session = scoped_session(sessionmaker(autoflush=False, autocommit=False, bind=engine))
