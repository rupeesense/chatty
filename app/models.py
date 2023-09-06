import uuid as uuid_pkg

import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    conversation_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('conversations.id'))
    sender = Column(String, nullable=False)  # 'user' or 'bot'
    content = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

#
# DATABASE_URL = "postgresql://avirlrma:@localhost:5432/chat_store"
#
# # Create tables in the database
# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(bind=engine)
