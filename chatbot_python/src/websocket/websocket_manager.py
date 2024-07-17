import asyncio
import typing

from fastapi import WebSocket


class WebSocketManager:
    _instance = None

    # Singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.active_connections: typing.Dict[str, WebSocket] = {}

    async def send(self, session_id: str, data: str):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_text(data)

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


websocket_manager = WebSocketManager()
