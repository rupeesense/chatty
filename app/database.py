from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://avirlrma:@localhost:5432/chat_store"

# Create a synchronous SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# This SessionLocal class is used to create and manage individual database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This Base class will be the class from which all of your models will inherit.
Base = declarative_base()
