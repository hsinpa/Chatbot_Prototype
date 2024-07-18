from typing import Optional

from pydantic import BaseModel, Field

from websocket.websocket_manager import WebSocketManager


class ChatbotInput(BaseModel):
    text: str
    session_id: str
    token: Optional[str]


class ChatbotStreamingInput(BaseModel):
    session_id: str
    token: str
