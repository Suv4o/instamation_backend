from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(f"postgresql://username:password@localhost/database_dev", echo=True)

db_session = scoped_session(sessionmaker(autoflush=False, autocommit=False, bind=engine))
