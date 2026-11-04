from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()
clients = {}
admins = {}

@app.websocket("/ws/{role}/{code}")
async def websocket_endpoint(websocket: WebSocket, role: str, code: str):
    await websocket.accept()
    if role == "client":
        clients[code] = websocket
        try:
            while True:
                data = await websocket.receive_text()
                if code in admins:
                    await admins[code].send_text(data)
        except WebSocketDisconnect:
            if code in clients: 
                del clients[code]
    elif role == "admin":
        admins[code] = websocket
        try:
            while True:
                data = await websocket.receive_text()
                if code in clients:
                    await clients[code].send_text(data)
        except WebSocketDisconnect:
            if code in admins: 
                del admins[code]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
