import uvicorn as uvicorn
from fastapi import FastAPI, WebSocketDisconnect, Header, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud import create_message, get_conversation_by_id, create_conversation, get_messages_by_conversation_id
from app.database import SessionLocal
from llm.chat_bot import Chatty

app = FastAPI()
chatty = Chatty()


@app.get("/")
def read_root():
    return {"message": "Hi from Chatty App!"}


# The header key would be X-User-ID/X-USER-ID
async def get_current_user(x_user_id: str = Header(None)) -> str:
    if x_user_id is None:
        raise WebSocketDisconnect()
    return x_user_id


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChatRequest(BaseModel):
    user_message: str = None
    conversation_id: str = None


class ConversationResponse(BaseModel):
    conversationId: str
    userId: str
    messages: list


@app.get("/chat/conversation/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conversation = get_conversation_by_id(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail=f"No conversation found with ID: {conversation_id}")

    messages = get_messages_by_conversation_id(db, conversation_id)

    return ConversationResponse(
        conversationId=conversation.id,  # Assuming conversation object has an 'id' attribute
        userId=conversation.user_id,  # Assuming conversation object has a 'user_id' attribute
        messages=messages  # This would be a list of message objects or dictionaries
    )


@app.post("/chat")
async def chat_endpoint(request: ChatRequest, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    if not request.user_message:
        raise HTTPException(status_code=400, detail="Content is required for the message.")

    if not request.conversation_id:
        # Start a new conversation
        conversation_id = create_conversation(db=db, user_id=user_id)
        message = f"New conversation started with ID: {conversation_id}"
    else:
        # Check if conversation exists, if not raise an error, else continue
        if not get_conversation_by_id(db=db, conversation_id=request.conversation_id):
            raise HTTPException(status_code=404, detail=f"No conversation found with ID: {request.conversation_id}")
        conversation_id = request.conversation_id
        message = f"Resumed conversation with ID: {conversation_id}"

    create_message(db=db,
                   conversation_id=conversation_id,
                   sender='user',
                   content=request.user_message,
                   user_id=user_id
                   )

    response = chatty.respond(message=request.user_message, chat_history=None)

    create_message(db=db,
                   conversation_id=conversation_id,
                   sender='system',
                   content=response,
                   user_id=user_id
                   )

    # For simplicity, echoing back the message with conversation status
    return {"response": response, "conversationId": conversation_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
