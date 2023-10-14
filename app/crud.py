import uuid

from sqlalchemy.orm import Session

from app.models import Conversation, Message


def create_conversation(db: Session, user_id: str):
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation.id


def create_message(db: Session, conversation_id: uuid.UUID, sender: str, content: str, user_id: str):
    message = Message(conversation_id=conversation_id, sender=sender, content=content, user_id=user_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message.id


def get_conversation_by_id(db: Session, conversation_id: str):
    return db.query(Conversation).filter(Conversation.id == uuid.UUID(conversation_id)).first()


def get_messages_by_conversation_id(db: Session, conversation_id: str):
    return db.query(Message).filter(Message.conversation_id == uuid.UUID(conversation_id))
