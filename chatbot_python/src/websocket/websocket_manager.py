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

    async def send(self, session_id: str, data: str):
        print('socket session', session_id)
        print('socket active_connections', self.active_connections)

        if session_id in self.active_connections:
            print('socket send', data)
            await self.active_connections[session_id].send_text(data)

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        print('active_connections', self.active_connections)

    def disconnect(self, session_id: str):
        print(f'socket disconnect {session_id}')

        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


websocket_manager = WebSocketManager()


def get_websocket():
    return websocket_manager
