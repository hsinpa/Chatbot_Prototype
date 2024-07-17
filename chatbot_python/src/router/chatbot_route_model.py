from typing import Optional

from pydantic import BaseModel


class ChatbotInput(BaseModel):
    text: str
    session_id: str
    token: Optional[str]


class ChatbotResponse(BaseModel):
    text: str
    session_id: str
    token_id: str
    index: int
