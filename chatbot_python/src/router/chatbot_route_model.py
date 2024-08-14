from typing import Optional

from pydantic import BaseModel


class ChatbotInput(BaseModel):
    text: str
    user_id: str
    session_id: str
    websocket_id: str
    token: Optional[str]


class ChatbotStreamingInput(BaseModel):
    session_id: str
    token: str
    websocket_id: str
