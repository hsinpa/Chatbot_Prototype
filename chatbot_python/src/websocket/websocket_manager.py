import asyncio
import typing

from fastapi import WebSocket


class WebSocketManager:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(WebSocketManager, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.active_connections: typing.Dict[str, WebSocket] = {}

    async def send(self, socket_id: str, data: str):
        if socket_id in self.active_connections:
            await self.active_connections[socket_id].send_text(data)

    async def connect(self, socket_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[socket_id] = websocket

    def disconnect(self, socket_id: str):
        if socket_id in self.active_connections:
            del self.active_connections[socket_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


websocket_manager = WebSocketManager()


def get_websocket():
    return websocket_manager
