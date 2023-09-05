from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, Header

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hi from Chatty App!"}


# The header key would be X-User-ID/X-USER-ID
async def get_current_user(x_user_id: str = Header(None)) -> str:
    if x_user_id is None:
        raise WebSocketDisconnect()
    return x_user_id

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, user_id: str = Depends(get_current_user)):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data} for user: {user_id}")
