import json
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from database.db_manager import PostgresDB_Chat
from src.router.chatbot_route import router as chatbot_router
from websocket.socket_static import SocketEvent
from websocket.websocket_manager import get_websocket

load_dotenv()

postgresDB = PostgresDB_Chat()

app = FastAPI(openapi_url="/docs/openapi.json", docs_url="/docs")
app.include_router(chatbot_router)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://counseling-psycho.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"version": "0.0.1"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    g_user_id = str(uuid.uuid4())
    print(g_user_id)
    websocket_manager = get_websocket()
    await websocket_manager.connect(g_user_id, websocket)
    try:
        await websocket.send_text(json.dumps({'event': SocketEvent.open, '_id': g_user_id}))

        while True:
            data = await websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        websocket_manager.disconnect(g_user_id)
