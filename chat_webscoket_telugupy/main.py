from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app =FastAPI()

app.mount("/static",StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    with open("static/chat.html","r") as f:
        return HTMLResponse(content=f.read(),status_code=200)
    
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)