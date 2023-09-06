import json

import uvicorn as uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Header, Depends
from sqlalchemy.orm import Session

from app.crud import create_message, get_conversation_by_id, create_conversation
from app.database import SessionLocal

app = FastAPI()


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


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


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, user_id: str = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    await websocket.accept()
    print("User ID2:")
    conversation_id = None

    while True:
        data = await websocket.receive_text()
        message_data = json.loads(data)

        # Handle start of a new conversation
        if message_data.get("type") == "start_conversation":
            conversation_id = create_conversation(db=db, user_id=user_id)
            await websocket.send_text(f"New conversation started with ID: {conversation_id}")
            continue

        # Handle resumption of an old conversation
        if message_data.get("type") == "resume_conversation":
            provided_conversation_id = message_data.get("conversationId")
            if provided_conversation_id:
                if get_conversation_by_id(db=db, conversation_id=provided_conversation_id):
                    conversation_id = provided_conversation_id
                    await websocket.send_text(f"Resumed conversation with ID: {conversation_id}")
                else:
                    await websocket.send_text(f"No conversation found with ID: {provided_conversation_id}")
            else:
                await websocket.send_text("Please provide a valid conversationId to resume.")
            continue

        # If conversation_id is not set at this point, raise an error.
        if not conversation_id:
            raise WebSocketDisconnect(code=400,
                                      reason="Please either start a new conversation or resume an existing one "
                                             "before sending messages.")

        # Handle regular chat messages
        create_message(db=db,
                       conversation_id=conversation_id,
                       sender='user',
                       content=message_data["content"],
                       user_id=user_id
                       )

        # TODO: Send message to bot and get response

        # For simplicity, we're just echoing the received message back.
        # In reality, you'd potentially process the message and generate a response.
        await websocket.send_text(f"Message received: {message_data['content']}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
